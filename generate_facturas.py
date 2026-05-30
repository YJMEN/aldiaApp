from app import app
from app import ensure_schema, ensure_admin_table_and_seed, generar_facturas_mensuales

if __name__ == "__main__":
    with app.app_context():
        ensure_schema()
        ensure_admin_table_and_seed()
        generar_facturas_mensuales()
        print("Facturas generadas correctamente.")
