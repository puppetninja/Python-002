# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings

from valkyrie_worker.items import ValkyriePhoneItem, ValkyriePhoneCommentItem


class ValkyrieWorkerPipeline:
    def process_item(self, item, spider):
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
                if isinstance(item, ValkyriePhoneItem):
                    sql = ("INSERT IGNORE INTO `phones` "
                           "(`phone_name`, `phone_url`) VALUES (%s, %s)")
                    cursor.execute(sql, (item['name'], item['url']))

                if isinstance(item, ValkyriePhoneCommentItem):
                    sql = ("INSERT INTO `phone_comments` "
                           "(`phone_name`, `comment_content`, `comment_date`) "
                           "VALUES (%s, %s, %s)")
                    cursor.execute(sql,
                                   (item['phone'], item['content'],
                                    item['date']))
                conn.commit()
        except Exception as e:
            print("Error encountered as {}".format(e))
            conn.rollback()
        finally:
            conn.close()
