

def populate_project_from_service_code(db_path, code):
    service = next(s for s in managersession().query(Service).all() if s.code.upper() == code)
    tasks = service.tasks
