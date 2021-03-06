@auth.requires_login()
def index():
    if not request.args:
        redirect(URL('error'))
    query = db.machine.id==request.args(0)
    return dict(rows = db(query).select(db.machine.id,
                                        db.machine.ip,
                                        db.machine.port,
                                        db.machine.name,
                                        db.miner.ALL,
                                        db.currency.ALL,
                                        db.pool.ALL,
                                        left=[db.platform.on(db.machine.platform_id==db.platform.id),
                                              db.platform_group.on(db.platform.group_id==db.platform_group.id),
                                              db.miner.on(db.platform_group.id==db.miner.plat_group_id),
                                              db.currency.on(db.miner.currency_id==db.currency.id),
                                              db.pool.on(db.miner.pool_id==db.pool.id)]))
