from app import app

if __name__ == "__main__":
    with app.app_context():
        from app import ensure_schema, ensure_admin_table_and_seed, generar_facturas_mensuales
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        ensure_schema()
        ensure_admin_table_and_seed()
        # Configurar scheduler para generar facturas mensuales
        scheduler = BackgroundScheduler()
        scheduler.add_job(generar_facturas_mensuales, CronTrigger(day=1, hour=0, minute=0))  # 1ro de cada mes a las 00:00
        scheduler.start()
    app.run(debug=True, port=5001)