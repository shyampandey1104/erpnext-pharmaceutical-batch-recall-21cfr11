"""Pharma 21 CFR Part 11 Electronic Batch Record (eBR) & Mock Recall Engine."""

import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class ElectronicSignature:
    signer_name: str
    signer_role: str  # QA_MANAGER, PRODUCTION_HEAD
    timestamp_utc: str
    signature_hash: str
    verdict: str  # APPROVED, REJECTED


@dataclass
class BatchDistributionRecord:
    batch_number: str
    product_code: str
    customer_id: str
    customer_name: str
    quantity_dispatched_vials: int
    invoice_number: str
    dispatch_date: str


@dataclass
class RecallExecutionSummary:
    batch_number: str
    product_code: str
    total_manufactured_vials: int
    total_quarantined_vials: int
    total_distributed_vials: int
    affected_customers_count: int
    recall_notification_list: List[Dict[str, Any]]
    is_recall_containment_complete: bool


class PharmaBatchRecallEngine:
    """FDA 21 CFR Part 11 dual-signoff audit and forward/backward drug batch trace controller."""

    def __init__(self):
        self.distributions: List[BatchDistributionRecord] = []

    def record_distribution(self, record: BatchDistributionRecord):
        self.distributions.append(record)

    def generate_electronic_signature(
        self,
        signer_name: str,
        signer_role: str,
        batch_number: str,
        timestamp_utc: str,
        verdict: str = "APPROVED"
    ) -> ElectronicSignature:
        raw_msg = f"{signer_name}|{signer_role}|{batch_number}|{timestamp_utc}|{verdict}"
        sig_hash = hashlib.sha256(raw_msg.encode("utf-8")).hexdigest()
        return ElectronicSignature(
            signer_name=signer_name,
            signer_role=signer_role,
            timestamp_utc=timestamp_utc,
            signature_hash=sig_hash,
            verdict=verdict
        )

    def execute_forward_batch_recall(
        self,
        batch_number: str,
        product_code: str,
        total_produced_vials: int,
        quarantined_in_warehouse_vials: int
    ) -> RecallExecutionSummary:
        matching_dispatches = [d for d in self.distributions if d.batch_number == batch_number]
        total_dispatched = sum(d.quantity_dispatched_vials for d in matching_dispatches)

        customer_map = {}
        for d in matching_dispatches:
            if d.customer_id not in customer_map:
                customer_map[d.customer_id] = {
                    "customer_name": d.customer_name,
                    "total_vials_to_quarantine": 0,
                    "invoices": []
                }
            customer_map[d.customer_id]["total_vials_to_quarantine"] += d.quantity_dispatched_vials
            customer_map[d.customer_id]["invoices"].append(d.invoice_number)

        notifications = [
            {"customer_id": cid, **meta}
            for cid, meta in customer_map.items()
        ]

        accounted = quarantined_in_warehouse_vials + total_dispatched
        is_contained = accounted == total_produced_vials

        return RecallExecutionSummary(
            batch_number=batch_number,
            product_code=product_code,
            total_manufactured_vials=total_produced_vials,
            total_quarantined_vials=quarantined_in_warehouse_vials,
            total_distributed_vials=total_dispatched,
            affected_customers_count=len(customer_map),
            recall_notification_list=notifications,
            is_recall_containment_complete=is_contained
        )
