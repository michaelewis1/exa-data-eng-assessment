import fhir
# transforming data into fhir objects
# def create_patient():

# def create_resource():

# def format_to_fhir():

def get_patient_info(entires) -> dict:
    # This function will be used to get the entities from the data
    for entry in entries:
        if entry.get("resourceType") == "Patient":
            patient = entry
            return patient
    pass