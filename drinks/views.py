from django.http import JsonResponse
from .serializers import DrinkSerializer
from .models import Drink
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def drink_list(request, format = None):
    # get all the drinks
    # serialize them
    # return json
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return JsonResponse({ 'drinks':serializer.data})
    
    if request.method == 'POST':
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])    
def drink_detail(request,id, format = None):
    try:
        drink = Drink.objects.get(pk = id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    






# LEARNING - ORM

def djangoorm(request, format=None):
    '''
    SELECT name,age FROM Person
    '''
    user = Drink.objects.only('name','age')

    '''
    SELECT DISTINCT name,age FROM Person
    '''
    user = Drink.objects.values('name','age').distinct()
    '''
    SELECT * FROM Person LIMIT 10;
    '''
    user = Drink.objects.all()[0:10]
    '''SELECT * FROM Person OFFSET 5 LIMIT 5;'''
    user = Drink.objects.all()[5:10]
    '''SELECT * FROM Person WHERE id = 1;'''
    user = Drink.objects.get(id=1)
    '''
    WHERE age > 18;
    WHERE age >= 18;
    WHERE age < 18;
    WHERE age <= 18;
    WHERE age != 18;'''
    user = Drink.objects.filter(age__gt=18)
    user = Drink.objects.filter(age__gte=18)
    user = Drink.objects.filter(age__lt=18)
    user= Drink.objects.filter(age__lte=18)
    user = Drink.objects.exclude(age=18)

    '''SELECT *
    FROM Person 
    WHERE age BETWEEN 10 AND 20;'''
    user = Drink.objects.filter(age__gte=10 , age__lt=20)
    user = Drink.objects.filter(age__range=(10,20))

    '''WHERE name like '%A%';
    WHERE name like binary '%A%';
    WHERE name like 'A%';
    WHERE name like binary 'A%';
    WHERE name like '%A';
    WHERE name like binary '%A';'''
    user = Drink.objects.filter(name__icontains='A')    # __icontains for case-in-sensitive substring match
    user = Drink.objects.filter(name__contains='A')   # __contains for case-sensitive substring match
    user = Drink.objects.filter(name__istartswith='A') # istartswith = case in-sensitive
    user = Drink.objects.filter(name__startswith='A')   # startswith = case sensitive
    user = Drink.objects.filter(name__iendswith='A') 
    user = Drink.objects.filter(name__endswith='A')

    '''WHERE id in (1, 2);'''
    user = Drink.objects.filter(id=[1,2])

    '''WHERE gender='male' AND age > 25;
    WHERE gender='male' OR age > 25;
    WHERE NOT gender='male';'''

    user = Drink.objects.filter(gender='male', age__gt=25)

    # for OR
    from django.db.models import Q
    user = Drink.objects.filter(Q(gender='male') | Q(age__gt=25))

    # NOT
    user = Drink.objects.exclude(gender='male')

    '''WHERE age is NULL;
    WHERE age is NOT NULL;'''
    user = Drink.objects.filter(age__isnull= True)
    user = Drink.objects.exclude(age__isnull= False) # or -> Drink.objects.exclude(age = None)

    '''SELECT * FROM Person order by age desc;
    SELECT * FROM Person order by age ;'''
    user = Drink.objects.all().order_by('-age') # age in desc
    user = Drink.objects.all().order_by('age') # age in asc

    '''INSERT INTO Person
    VALUES ('Jack', '23', 'male');'''

    user = Drink.objects.create(name='Jack', age=23, gender='male')

    '''UPDATE Person
    SET age = 20
    WHERE id = 1;'''
    user = Drink.objects.filter(id=1)
    user.age = 20
    user.save()

    '''UPDATE Person
    SET age = age * 1.5;'''
    from django.db.models import F
    user = Drink.objects.update(age= F('age')*1.5)

    '''Delete all the rows -> DELETE FROM Person;'''
    user = Drink.objects.all().delete()

    '''DELETE FROM Person
    WHERE age < 10;'''
    user = Drink.objects.filter(age__lt=10).delete()

    '''SELECT MIN(age)
    FROM Person;'''
    from django.db.models import Min
    user = Drink.objects.all().aggregate(Min('age'))

    '''SELECT MAX(age)
    FROM Person;'''
    from django.db.models import Max
    user = Drink.objects.all().aggregate(Max('age'))

    '''SELECT AVG(age)
    FROM Person;'''
    from django.db.models import Avg
    user = Drink.objects.all().aggregate(Avg('age'))

    '''SELECT SUM(age)
    FROM Person;'''
    from django.db.models import Sum
    user = Drink.objects.all().aggregate(Sum('age'))

    '''SELECT COUNT(*)
    FROM Person;'''
    user = Drink.objects.count()

    '''SELECT gender, COUNT(*) as count
    FROM Person
    GROUP BY gender;'''
    from django.db.models import Count
    user = Drink.objects.values('gender').annotate(count=Count('count'))

    '''SELECT gender, COUNT('gender') as count
    FROM Person
    GROUP BY gender
    HAVING count > 1;'''
    user = Drink.objects.annotate(count=Count('gender')).values('gender', 'count').filter(count__gt=1)


