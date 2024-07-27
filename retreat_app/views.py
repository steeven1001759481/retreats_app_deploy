from django.shortcuts import render
from django.http import JsonResponse
from retreat_app.models import Retreats,Bookings, Session
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import or_
import json

def get_retreats(request):
    session = Session()
    params = request.GET.dict()
    global retreats
    if 'filter' in params:
        filterKeyword = params['filter']
        retreats = session.query(Retreats).filter(or_(
            Retreats.title.ilike(f"%{filterKeyword}%"),
            Retreats.description.ilike(f"%{filterKeyword}%"),
            Retreats.location.ilike(f"%{filterKeyword}%"),
            Retreats.retype.ilike(f"%{filterKeyword}%"),
            Retreats.condition.ilike(f"%{filterKeyword}%"))
            )
    elif 'search' in params:
        filterKeyword = params['search']
        retreats = session.query(Retreats).filter(or_(
            Retreats.title.ilike(f"%{filterKeyword}%"),
            Retreats.description.ilike(f"%{filterKeyword}%"),
            Retreats.location.ilike(f"%{filterKeyword}%"),
            Retreats.retype.ilike(f"%{filterKeyword}%"),
            Retreats.condition.ilike(f"%{filterKeyword}%"))
            )
    elif 'page' in params:
        retreats = session.query(Retreats).all()
        pageNumber = int(params['page'])
        limit = int(params['limit'])
        start = ((pageNumber) - 1) * limit
        end = start + limit
        retreats = retreats[start:end]
    elif params:
        for k, v in params.items():
            keywordFilter = k
            filterValue = v
        if keywordFilter == 'type':
            f = Retreats.retype
        else:
            f = getattr(Retreats, keywordFilter)
        retreats = session.query(Retreats).filter(or_(f==params[keywordFilter], f==params[keywordFilter].lower()))
    else:
        retreats = session.query(Retreats).all()

    retreat_list = [{'id': r.id, 'title': r.title, 'description':r.description, 'date': r.date, 'location': r.location, 'price': r.price, 'type':r.retype, 'condition': r.condition, 'image': r.image, 'tag':r.tag, 'duration': r.duration} for r in retreats]
    session.close()

    return JsonResponse(retreat_list, safe=False)

def get_bookings(request):
    session = Session()
    booking_data = session.query(Bookings).all()
    print(booking_data)
    booking_list = [{'id': b.user_id, 'username': b.user_name, 'title': b.retreat_title} for b in booking_data]
    session.close()

    return JsonResponse(booking_list, safe=False)


@csrf_exempt
def book_retreat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session = Session()
        retreat = session.query(Retreats).filter_by(id=data['retreat_id']).first()
        if retreat:
            booking = session.query(Bookings).filter_by(user_id=data['user_id'], retreat_id=data['retreat_id']).first()
            if not booking:
                booking = Bookings(
                    user_id=data['user_id'],
                    user_name=data['user_name'],
                    user_email=data['user_email'],
                    user_phone=data['user_phone'],
                    retreat_id=retreat.id,
                    retreat_title=data['retreat_title'],
                    retreat_location=data['retreat_location'],
                    retreat_price=data['retreat_price'],
                    retreat_duration=data['retreat_duration'],
                    payment_details=data['payment_details'],
                    booking_date=data['booking_date'],
                )
                session.add(booking)
                session.commit()
                session.close()
                return JsonResponse({'message': 'Booking created successfully'}, status=201)
            else:
                session.close()
                return JsonResponse({'message': 'Booking already exists'}, status=400)
        else:
            session.close()
            return JsonResponse({'error': 'Retreat not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
