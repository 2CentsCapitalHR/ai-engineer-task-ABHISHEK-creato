from typing import List, Dict

class ChecklistVerifier:
    def __init__(self):
        self.checklists = {
            "Company Incorporation": [
                "Articles of Association",
                "Memorandum of Association",
                "Incorporation Application Form",
                "UBO Declaration Form",
                "Register of Members and Directors"
            ],
            "Licensing": [
                "License Application Form",
                "Business Plan",
                "Shareholder Information"
            ]
        }
    
    def verify_documents(self, process_type: str, uploaded_docs: List[str]) -> Dict:
        required = self.checklists.get(process_type, [])
        uploaded_types = [doc['type'] for doc in uploaded_docs]
        
        missing = [doc for doc in required if doc not in uploaded_types]
        
        return {
            "process": process_type,
            "documents_uploaded": len(uploaded_docs),
            "required_documents": len(required),
            "missing_documents": missing,
            "all_documents_present": len(missing) == 0
        }