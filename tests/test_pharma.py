import unittest
from pharma.engine import PharmaBatchRecallEngine, BatchDistributionRecord

class TestPharmaBatchRecall(unittest.TestCase):
    def test_e_signature_and_forward_recall(self):
        engine = PharmaBatchRecallEngine()

        sig = engine.generate_electronic_signature(
            signer_name="Dr. Sunita Rao",
            signer_role="QA_MANAGER",
            batch_number="VAX-2026-B81",
            timestamp_utc="2026-11-14T08:00:00Z"
        )
        self.assertEqual(len(sig.signature_hash), 64)
        self.assertEqual(sig.verdict, "APPROVED")

        engine.record_distribution(BatchDistributionRecord(
            batch_number="VAX-2026-B81",
            product_code="COV-INJ-50ML",
            customer_id="HOSP-01",
            customer_name="Apollo Hospitals Mumbai",
            quantity_dispatched_vials=400,
            invoice_number="INV-2026-901",
            dispatch_date="2026-11-01"
        ))
        engine.record_distribution(BatchDistributionRecord(
            batch_number="VAX-2026-B81",
            product_code="COV-INJ-50ML",
            customer_id="HOSP-02",
            customer_name="Fortis Healthcare Delhi",
            quantity_dispatched_vials=600,
            invoice_number="INV-2026-902",
            dispatch_date="2026-11-02"
        ))

        summary = engine.execute_forward_batch_recall(
            batch_number="VAX-2026-B81",
            product_code="COV-INJ-50ML",
            total_produced_vials=1500,
            quarantined_in_warehouse_vials=500
        )

        self.assertEqual(summary.total_distributed_vials, 1000)
        self.assertEqual(summary.affected_customers_count, 2)
        self.assertTrue(summary.is_recall_containment_complete)

if __name__ == "__main__":
    unittest.main()
