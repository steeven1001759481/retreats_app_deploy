import requests
from django.core.management.base import BaseCommand
from retreat_app.models import Retreats, engine, Session

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        response = requests.get('https://669f704cb132e2c136fdd9a0.mockapi.io/api/v1/retreats')
        if response.status_code == 200:
            retreats = response.json()
            session = Session()
            for retreat_data in retreats:
                retreat = session.query(Retreats).filter_by(id=retreat_data['id']).first()
                if not retreat:
                    retreat = Retreats(id=retreat_data['id'])
                retreat.title = retreat_data['title']
                retreat.description = retreat_data['description']
                retreat.date = retreat_data['date']
                retreat.location = retreat_data['location']
                retreat.price = retreat_data['price']
                retreat.retype = retreat_data['type']
                retreat.condition = retreat_data['condition']
                retreat.image = retreat_data['image']
                retreat.tag = retreat_data['tag']
                retreat.duration = retreat_data['duration']
                session.add(retreat)
            session.commit()
            session.close()
            self.stdout.write(self.style.SUCCESS('Successfully populated the database with retreat data'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch retreat data'))
