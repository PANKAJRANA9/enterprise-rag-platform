from src.models.document import Document
from typing import List

class DataGeneratorService:
    def get_odoo_data(self) -> List[dict]:
        return [
            {"text":"Invoice INV-1001 for Acme Corp is overdue by 15 days, amount Rs 50000, due date 2025-10-15", "meta":{"type":"invoice","id":"INV-1001","customer":"Acme"}},
            {"text":"Product 【entity-Dell¦canonical_name=Dell】 XPS 13 Laptop stock is 5 units in Warehouse A, reorder level 10", "meta":{"type":"inventory","product":"【entity-Dell¦canonical_name=Dell】 XPS"}},
            {"text":"Purchase Order PO-202 for 20 office chairs approved by finance", "meta":{"type":"po"}},
        ]

    def get_crm_data(self) -> List[dict]:
        return [
            {"text":"Client Acme Corp complained about pricing on 20th Oct, said competitor offers 10% lower", "meta":{"customer":"Acme","type":"ticket","priority":"high"}},
            {"text":"Meeting notes with Priya from Acme on 22 Oct - interested in premium plan budget 2L, follow up next week", "meta":{"customer":"Acme","type":"meeting"}},
            {"text":"Lead 【entity-Infosys¦canonical_name=Infosys】 wants demo for 【entity-Odoo¦canonical_name=Odoo】 CRM customization", "meta":{"customer":"【entity-Infosys¦canonical_name=Infosys】","type":"lead"}},
        ]

    def get_parking_data(self) -> List[dict]:
        return [
            {"text":"Parking Rule: EV vehicles allowed free parking for 2 hours in Slot A, FASTag not required", "meta":{"type":"rule","zone":"A"}},
            {"text":"Incident: Vehicle DL01AB1234 overstayed 5 hours in Basement 2 on 2025-10-10, fine Rs 500", "meta":{"type":"incident"}},
            {"text":"Slot B2 sensor faulty reported on 12th Oct, needs maintenance", "meta":{"type":"maintenance"}},
        ]

    def get_medical_data(self) -> List[dict]:
        return [
            {"text":"ICMR Guideline: For children fever >2 days with cold, maintain hydration, monitor temperature every 4 hours. Consult pediatrician if >101F persists", "meta":{"source":"icmr_guideline","type":"fever"}},
            {"text":"Drug Info: Paracetamol dosage for children 10-15mg/kg per dose, max 4 doses per day", "meta":{"source":"drug_book"}},
            {"text":"Practo FAQ: Appointment booking requires patient name, age, symptoms. Cancel allowed 2 hours before", "meta":{"source":"faq"}},
        ]

    def get_whatsapp_data(self) -> List[dict]:
        return [
            {"text":"NCERT Geography: Atmosphere has 5 layers - Troposphere, Stratosphere, Mesosphere, Thermosphere, Exosphere", "meta":{"subject":"geography","chapter":"3"}},
            {"text":"Photosynthesis is process used by plants to convert light energy into chemical energy, requires CO2 and water", "meta":{"subject":"science"}},
        ]