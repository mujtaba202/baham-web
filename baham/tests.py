# Create your tests here.

from django.test import TestCase
from django.contrib.auth.models import User
from baham.models import UserProfile, Vehicle, Contract, VehicleModel

class VehicleContractTestCase(TestCase):
    def setUp(self):
        self.userOwner = User.objects.create_user(username='KHAN', password='Password')
        self.userprofileOwner = UserProfile.objects.create(user=self.userOwner, birthdate="1990-09-10", type='OWNER')
        self.vehicleModel = VehicleModel.objects.create(vendor="Toyota", model="COROLLA", type="CAR", capacity="1")
        self.vehicle = Vehicle.objects.create(registration_number='KNP-999', model=self.vehicleModel, owner=self.userOwner)
        self.userCompanion = User.objects.create_user(username='Companion', password='Password')
        self.userprofileCompanion = UserProfile.objects.create(user=self.userCompanion,birthdate="1998-01-01", type='COMPANION')
        self.contract = Contract.objects.create(vehicle=self.vehicle, effective_start_date="2023-03-01",expiry_date="2024-03-01", 
                                                fuel_share="60", 
                                                maintenance_share="60", 
                                                companion=self.userprofileCompanion, 
                                                is_active=True)

    def test_one_vehicle_per_owner(self):
        with self.assertRaises(Exception):
            Vehicle.objects.create(registration_number='KNP-101', model=self.vehicleModel, owner=self.userOwner)

    def test_passengers_capacity(self):
        with self.assertRaises(Exception):
            Contract.objects.create(vehicle=self.vehicle, effective_start_date="2023-03-01",expiry_date="2024-03-01", 
                                    fuel_share="60",
                                    maintenance_share="60", 
                                    companion=self.userprofileCompanion, is_active=True)
        

    def test_total_share(self):
        invalid_contract = Contract.objects.create(vehicle=self.vehicle,
                                                   companion=self.userprofileCompanion,
                                                   effective_start_date="2023-03-01",
                                                   expiry_date="2024-03-01",
                                                   is_active=True,
                                                   fuel_share=60, 
                                                   maintenance_share=60)
        self.assertLessEqual(invalid_contract.fuel_share + invalid_contract.maintenance_share, 100)

    def test_multiple_active_contracts(self):
        invalid_contract = Contract.objects.create(vehicle=self.vehicle,
                                                    companion=self.userprofileCompanion,
                                                    effective_start_date="2023-01-09",
                                                    expiry_date="2023-03-15",
                                                    is_active=True,
                                                    fuel_share=60,
                                                    maintenance_share=90)
        self.assertFalse(invalid_contract.is_active)
        
    def tearDown(self):
        UserProfile.objects.all().delete()
        Vehicle.objects.all().delete()
        Contract.objects.all().delete()
        User.objects.all().delete()
