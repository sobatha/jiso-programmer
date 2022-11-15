'''
ログには5W1Hを記載する
'''

def main():
    try:
        logger.info("売上CSV取込開始")

        sales_date=load_sales_csv()
        logger.info("売上CSV取込済")

        for code, sales_rows in sales_data:
            logger.info("取込開始 - 店舗コード: %s, データ件数: %s", code, len(sales_rows))
            
            try:
                for i, row in enumurate(sales_rows, start=1):
                    logger.debug("取込処理中 - 店舗(%s) %s行目: エラー%s", code, i, exc, exc_info=True)
                    continue
                logger.info("取込正常終了 - 店舗コード: %s", code)

        logger.info("売上CSV取込処理完了")
    except Exception as exc:
        logger.error('売上CSV取込処理で予期しないエラー発生: エラー %s', exc, exc_info=True)
