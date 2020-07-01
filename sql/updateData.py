import datetime

import loguru
import sqlalchemy
import sqlalchemy.ext.automap
import sqlalchemy.orm
import sqlalchemy.schema

def main():
    username = 'root'     # 資料庫帳號
    password = 'root'     # 資料庫密碼
    host = 'localhost'    # 資料庫位址
    port = '3306'         # 資料庫埠號
    database = 'trader'   # 資料庫名稱
    # 建立連線引擎
    engine = sqlalchemy.create_engine(
        f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    )
    metadata = sqlalchemy.schema.MetaData(engine)
    automap = sqlalchemy.ext.automap.automap_base()
    automap.prepare(engine, reflect=True)
    session = sqlalchemy.orm.Session(engine)

    sqlalchemy.Table('stocks', metadata, autoload=True)
    Stock = automap.classes['stocks']

    loguru.logger.info('----- 更新單筆資料 -----')
    try:
        stock = session.query(Stock).filter(
            Stock.code == '1102'
        ).one()
        stock.name = stock.name + '（水泥產業）'
        session.add(stock)

        # 寫入資料庫
        session.commit()
    except Exception as e:
        # 發生例外錯誤，還原交易
        session.rollback()
        loguru.logger.error('更新資料失敗')
        loguru.logger.error(e)

    loguru.logger.info('取出資料表所有資料')
    results = session.query(Stock).all()
    for stock in results:
        loguru.logger.info(f'{stock.code} {stock.name}')

    loguru.logger.info('----- 更新多筆資料 -----')
    try:
        session.query(Stock).filter(
            sqlalchemy.and_(
                Stock.code.like('11%'),
                Stock.code != '1102'
            )
        ).update({
            Stock.name: Stock.name + '（水泥產業）'
        }, synchronize_session=False)

        # 寫入資料庫
        session.commit()
    except Exception as e:
        # 發生例外錯誤，還原交易
        session.rollback()
        loguru.logger.error('更新資料失敗')
        loguru.logger.error(e)

    loguru.logger.info('取出資料表所有資料')
    results = session.query(Stock).all()
    for stock in results:
        loguru.logger.info(f'{stock.code} {stock.name}')

    session.close()

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    main()