from app import app

if __name__ == "__main__":
    with app.app_context():
        from app import ensure_schema, ensure_admin_table_and_seed, generar_facturas_mensuales
        ensure_schema()
        ensure_admin_table_and_seed()
        if app.config.get("ENABLE_SCHEDULER"):
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            scheduler = BackgroundScheduler()
            scheduler.add_job(generar_facturas_mensuales, CronTrigger(day=1, hour=0, minute=0))
            scheduler.start()

    debug = app.config.get("FLASK_DEBUG", False)
    port = app.config.get("PORT", 5001)
    app.run(debug=debug, port=port)