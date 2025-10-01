import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal, engine, Base
from app.models import Building, Activity, Organization, PhoneNumber
from sqlalchemy import text, select


async def create_tables():
    """Создание всех таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_data():
    """Заполнение тестовыми данными"""
    db = AsyncSessionLocal()
    try:
        # Проверяем, есть ли уже данные в базе
        result = await db.execute(select(Organization).limit(1))
        existing_org = result.scalar_one_or_none()
        
        if existing_org:
            print("Тестовые данные уже существуют, пропускаем заполнение")
            return
        # Создаем здания
        buildings_data = [
            {
                "address": "г. Москва, ул. Ленина, д. 1, офис 3",
                "latitude": 55.7558,
                "longitude": 37.6176
            },
            {
                "address": "г. Москва, ул. Мира, д. 32",
                "latitude": 55.7600,
                "longitude": 37.6200
            },
            {
                "address": "г. Москва, ул. Тверская, д. 10",
                "latitude": 55.7500,
                "longitude": 37.6100
            },
            {
                "address": "г. Санкт-Петербург, Невский проспект, д. 4",
                "latitude": 59.9311,
                "longitude": 30.3609
            }
        ]
        
        buildings = []
        for building_data in buildings_data:
            building = Building(**building_data)
            db.add(building)
            buildings.append(building)
        
        await db.commit()
    
        activities_data = [
            {"name": "Еда", "parent_id": None, "level": 1},
            {"name": "Автомобили", "parent_id": None, "level": 1},
            {"name": "Одежда", "parent_id": None, "level": 1},
            
            {"name": "Мясная продукция", "parent_id": None, "level": 2},
            {"name": "Молочная продукция", "parent_id": None, "level": 2},
            {"name": "Хлебобулочные изделия", "parent_id": None, "level": 2},
            
            {"name": "Грузовые", "parent_id": None, "level": 2},
            {"name": "Легковые", "parent_id": None, "level": 2},
            
            {"name": "Запчасти", "parent_id": None, "level": 3},
            {"name": "Аксессуары", "parent_id": None, "level": 3},
        ]
        
        activities = []
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
            activities.append(activity)
        
        await db.commit()
    
        
        activities[3].parent_id = activities[0].id  # Мясная продукция -> Еда
        activities[4].parent_id = activities[0].id  # Молочная продукция -> Еда
        activities[5].parent_id = activities[0].id  # Хлебобулочные изделия -> Еда
        
        activities[6].parent_id = activities[1].id  # Грузовые -> Автомобили
        activities[7].parent_id = activities[1].id  # Легковые -> Автомобили
        
        activities[8].parent_id = activities[7].id  # Запчасти -> Легковые
        activities[9].parent_id = activities[7].id  # Аксессуары -> Легковые
        
        await db.commit()
    
        organizations_data = [
            {
                "name": 'ООО "Рога и Копыта"',
                "building_id": buildings[0].id,
                "phone_numbers": ["2-222-222", "3-333-333", "8-923-666-13-13"],
                "activity_ids": [activities[3].id, activities[4].id]
            },
            {
                "name": 'ООО "Мясной царь"',
                "building_id": buildings[1].id,
                "phone_numbers": ["8-800-555-35-35"],
                "activity_ids": [activities[3].id]
            },
            {
                "name": 'ООО "Молоко"',
                "building_id": buildings[2].id,
                "phone_numbers": ["+7-495-123-45-67", "8-926-123-45-67"],
                "activity_ids": [activities[4].id]
            },
            {
                "name": 'ООО "АвтоГруз"',
                "building_id": buildings[0].id,
                "phone_numbers": ["8-800-200-00-00"],
                "activity_ids": [activities[6].id]
            },
            {
                "name": 'ООО "Легковые"',
                "building_id": buildings[1].id,
                "phone_numbers": ["8-495-999-88-77"],
                "activity_ids": [activities[7].id, activities[8].id, activities[9].id]
            },
            {
                "name": 'ООО "Хлеб"',
                "building_id": buildings[3].id,
                "phone_numbers": ["8-812-555-12-34"],
                "activity_ids": [activities[5].id]
            },
            {
                "name": 'ООО "Модник"',
                "building_id": buildings[2].id,
                "phone_numbers": ["8-495-777-66-55"],
                "activity_ids": [activities[2].id]
            }
        ]
    
        for org_data in organizations_data:
            phone_numbers = org_data.pop("phone_numbers")
            activity_ids = org_data.pop("activity_ids")
            
            organization = Organization(**org_data)
            db.add(organization)
            await db.flush()
            
            for phone_num in phone_numbers:
                phone = PhoneNumber(number=phone_num, organization_id=organization.id)
                db.add(phone)
            
            for activity_id in activity_ids:
                activity = await db.get(Activity, activity_id)
                if activity:
                    await db.execute(text(
                        "INSERT INTO organization_activities (organization_id, activity_id) VALUES (:org_id, :act_id)"
                    ), {"org_id": organization.id, "act_id": activity_id})
        
        await db.commit()
        print("Тестовые данные успешно добавлены!")
        
    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")
        raise
    finally:
        await db.close()

async def main():
    await create_tables()
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())