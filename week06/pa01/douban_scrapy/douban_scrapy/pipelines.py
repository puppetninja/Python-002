# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings

import pymysql


class DoubanScrapyPipeline:
    def process_item(self, item, spider):
        if item is not None:
            db_info = get_project_settings().get('DB_INFO')

            conn = pymysql.connect(
                host=db_info['host'],
                port=db_info['port'],
                user=db_info['user'],
                password=db_info['password'],
                db=db_info['db'],
                charset=db_info['charset']
            )

            try:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO `movie_reviews` (`review_rating`, `review_content`) VALUES (%s, %s)"
                    cursor.execute(sql,
                                   (item['rating'], item['comment']))
                conn.commit()
            except Exception as e:
                print("Error encountered as {}".format(e))
                conn.rollback()
            finally:
                conn.close()

        return item
