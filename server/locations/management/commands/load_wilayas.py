from django.core.management.base import BaseCommand
from locations.models import Wilaya

class Command(BaseCommand):
    help = 'Load Algerian wilayas data into the database'
    
    def handle(self, *args, **options):
        wilayas_data = [
            {'code': '01', 'name_ar': 'أدرار', 'name_en': 'Adrar', 'name_fr': 'Adrar'},
            {'code': '02', 'name_ar': 'الشلف', 'name_en': 'Chlef', 'name_fr': 'Chlef'},
            {'code': '03', 'name_ar': 'الأغواط', 'name_en': 'Laghouat', 'name_fr': 'Laghouat'},
            {'code': '04', 'name_ar': 'أم البواقي', 'name_en': 'Oum El Bouaghi', 'name_fr': 'Oum El Bouaghi'},
            {'code': '05', 'name_ar': 'باتنة', 'name_en': 'Batna', 'name_fr': 'Batna'},
            {'code': '06', 'name_ar': 'بجاية', 'name_en': 'Bejaia', 'name_fr': 'Béjaïa'},
            {'code': '07', 'name_ar': 'بسكرة', 'name_en': 'Biskra', 'name_fr': 'Biskra'},
            {'code': '08', 'name_ar': 'بشار', 'name_en': 'Bechar', 'name_fr': 'Béchar'},
            {'code': '09', 'name_ar': 'البليدة', 'name_en': 'Blida', 'name_fr': 'Blida'},
            {'code': '10', 'name_ar': 'البويرة', 'name_en': 'Bouira', 'name_fr': 'Bouira'},
            {'code': '11', 'name_ar': 'تمنراست', 'name_en': 'Tamanrasset', 'name_fr': 'Tamanrasset'},
            {'code': '12', 'name_ar': 'تبسة', 'name_en': 'Tebessa', 'name_fr': 'Tébessa'},
            {'code': '13', 'name_ar': 'تلمسان', 'name_en': 'Tlemcen', 'name_fr': 'Tlemcen'},
            {'code': '14', 'name_ar': 'تيارت', 'name_en': 'Tiaret', 'name_fr': 'Tiaret'},
            {'code': '15', 'name_ar': 'تيزي وزو', 'name_en': 'Tizi Ouzou', 'name_fr': 'Tizi Ouzou'},
            {'code': '16', 'name_ar': 'الجزائر', 'name_en': 'Algiers', 'name_fr': 'Alger'},
            {'code': '17', 'name_ar': 'الجلفة', 'name_en': 'Djelfa', 'name_fr': 'Djelfa'},
            {'code': '18', 'name_ar': 'جيجل', 'name_en': 'Jijel', 'name_fr': 'Jijel'},
            {'code': '19', 'name_ar': 'سطيف', 'name_en': 'Setif', 'name_fr': 'Sétif'},
            {'code': '20', 'name_ar': 'سعيدة', 'name_en': 'Saida', 'name_fr': 'Saïda'},
            {'code': '21', 'name_ar': 'سكيكدة', 'name_en': 'Skikda', 'name_fr': 'Skikda'},
            {'code': '22', 'name_ar': 'سيدي بلعباس', 'name_en': 'Sidi Bel Abbes', 'name_fr': 'Sidi Bel Abbès'},
            {'code': '23', 'name_ar': 'عنابة', 'name_en': 'Annaba', 'name_fr': 'Annaba'},
            {'code': '24', 'name_ar': 'قالمة', 'name_en': 'Guelma', 'name_fr': 'Guelma'},
            {'code': '25', 'name_ar': 'قسنطينة', 'name_en': 'Constantine', 'name_fr': 'Constantine'},
            {'code': '26', 'name_ar': 'المدية', 'name_en': 'Medea', 'name_fr': 'Médéa'},
            {'code': '27', 'name_ar': 'مستغانم', 'name_en': 'Mostaganem', 'name_fr': 'Mostaganem'},
            {'code': '28', 'name_ar': 'المسيلة', 'name_en': 'Msila', 'name_fr': 'M\'Sila'},
            {'code': '29', 'name_ar': 'معسكر', 'name_en': 'Mascara', 'name_fr': 'Mascara'},
            {'code': '30', 'name_ar': 'ورقلة', 'name_en': 'Ouargla', 'name_fr': 'Ouargla'},
            {'code': '31', 'name_ar': 'وهران', 'name_en': 'Oran', 'name_fr': 'Oran'},
            {'code': '32', 'name_ar': 'البيض', 'name_en': 'El Bayadh', 'name_fr': 'El Bayadh'},
            {'code': '33', 'name_ar': 'إليزي', 'name_en': 'Illizi', 'name_fr': 'Illizi'},
            {'code': '34', 'name_ar': 'برج بوعريريج', 'name_en': 'Bordj Bou Arreridj', 'name_fr': 'Bordj Bou Arréridj'},
            {'code': '35', 'name_ar': 'بومرداس', 'name_en': 'Boumerdes', 'name_fr': 'Boumerdès'},
            {'code': '36', 'name_ar': 'الطارف', 'name_en': 'El Tarf', 'name_fr': 'El Tarf'},
            {'code': '37', 'name_ar': 'تندوف', 'name_en': 'Tindouf', 'name_fr': 'Tindouf'},
            {'code': '38', 'name_ar': 'تيسمسيلت', 'name_en': 'Tissemsilt', 'name_fr': 'Tissemsilt'},
            {'code': '39', 'name_ar': 'الوادي', 'name_en': 'El Oued', 'name_fr': 'El Oued'},
            {'code': '40', 'name_ar': 'خنشلة', 'name_en': 'Khenchela', 'name_fr': 'Khenchela'},
            {'code': '41', 'name_ar': 'سوق أهراس', 'name_en': 'Souk Ahras', 'name_fr': 'Souk Ahras'},
            {'code': '42', 'name_ar': 'تيبازة', 'name_en': 'Tipaza', 'name_fr': 'Tipaza'},
            {'code': '43', 'name_ar': 'ميلة', 'name_en': 'Mila', 'name_fr': 'Mila'},
            {'code': '44', 'name_ar': 'عين الدفلى', 'name_en': 'Ain Defla', 'name_fr': 'Aïn Defla'},
            {'code': '45', 'name_ar': 'النعامة', 'name_en': 'Naama', 'name_fr': 'Naâma'},
            {'code': '46', 'name_ar': 'عين تموشنت', 'name_en': 'Ain Temouchent', 'name_fr': 'Aïn Témouchent'},
            {'code': '47', 'name_ar': 'غرداية', 'name_en': 'Ghardaia', 'name_fr': 'Ghardaïa'},
            {'code': '48', 'name_ar': 'غليزان', 'name_en': 'Relizane', 'name_fr': 'Relizane'},
            {'code': '49', 'name_ar': 'تيميمون', 'name_en': 'Timimoun', 'name_fr': 'Timimoun'},
            {'code': '50', 'name_ar': 'برج باجي مختار', 'name_en': 'Bordj Badji Mokhtar', 'name_fr': 'Bordj Badji Mokhtar'},
            {'code': '51', 'name_ar': 'أولاد جلال', 'name_en': 'Ouled Djellal', 'name_fr': 'Ouled Djellal'},
            {'code': '52', 'name_ar': 'بني عباس', 'name_en': 'Beni Abbes', 'name_fr': 'Béni Abbès'},
            {'code': '53', 'name_ar': 'عين صالح', 'name_en': 'In Salah', 'name_fr': 'In Salah'},
            {'code': '54', 'name_ar': 'عين قزام', 'name_en': 'In Guezzam', 'name_fr': 'In Guezzam'},
            {'code': '55', 'name_ar': 'توقرت', 'name_en': 'Touggourt', 'name_fr': 'Touggourt'},
            {'code': '56', 'name_ar': 'جانت', 'name_en': 'Djanet', 'name_fr': 'Djanet'},
            {'code': '57', 'name_ar': 'المقرة', 'name_en': 'El Meghaier', 'name_fr': 'El M\'Ghair'},
            {'code': '58', 'name_ar': 'المنيعة', 'name_en': 'El Menia', 'name_fr': 'El Ménéa'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for wilaya_data in wilayas_data:
            wilaya, created = Wilaya.objects.get_or_create(
                code=wilaya_data['code'],
                defaults=wilaya_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created wilaya: {wilaya.code} - {wilaya.name_en}')
                )
            else:
                # Update existing wilaya if data has changed
                updated = False
                for field, value in wilaya_data.items():
                    if getattr(wilaya, field) != value:
                        setattr(wilaya, field, value)
                        updated = True
                
                if updated:
                    wilaya.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated wilaya: {wilaya.code} - {wilaya.name_en}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded wilayas: {created_count} created, {updated_count} updated'
            )
        )
