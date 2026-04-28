import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from main_app.models import Report


class Command(BaseCommand):
    help = "Generate dummy report data until the total report count reaches the target."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=600,
            help="Target total number of reports in the database.",
        )

    def handle(self, *args, **options):
        target_count = max(options["count"], 0)
        current_count = Report.objects.count()

        if current_count >= target_count:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Data laporan sudah berjumlah {current_count}. Tidak perlu menambah data dummy."
                )
            )
            return

        categories = [
            "Jalan Rusak",
            "Lampu Jalan",
            "Sampah",
            "Drainase",
            "Taman Kota",
            "Air Bersih",
            "Kemacetan",
            "Trotoar",
            "Keamanan",
            "Fasilitas Umum",
        ]
        locations = [
            "Terminal Rajabasa",
            "Jl. ZA Pagar Alam",
            "Jl. Soekarno Hatta",
            "Kecamatan Sukarame",
            "Kecamatan Kedaton",
            "Area Kampus Polinela",
            "Pasar Bambu Kuning",
            "Jl. Teuku Umar",
            "Way Halim",
            "Labuhan Ratu",
        ]
        names = [
            "Andi",
            "Budi",
            "Citra",
            "Dewi",
            "Eka",
            "Fajar",
            "Gita",
            "Hani",
            "Indra",
            "Joko",
            "Kartika",
            "Lina",
            "Maya",
            "Nadia",
            "Putra",
            "Rani",
            "Sinta",
            "Teguh",
            "Vina",
            "Yusuf",
        ]
        title_templates = [
            "Laporan {category} di {location}",
            "{category} membutuhkan penanganan di {location}",
            "Permasalahan {category} sekitar {location}",
            "{category} warga area {location}",
            "Tindak lanjut {category} pada {location}",
        ]
        description_templates = [
            "Warga melaporkan kondisi {category_lower} yang perlu segera ditangani di area {location}.",
            "Masalah {category_lower} sudah terjadi beberapa hari dan mengganggu aktivitas masyarakat di {location}.",
            "Diperlukan tindak lanjut dari pihak terkait karena kondisi {category_lower} di {location} semakin mengganggu.",
            "Laporan ini dibuat agar petugas dapat meninjau permasalahan {category_lower} yang ditemukan di {location}.",
        ]
        statuses = [
            Report.STATUS_REPORTED,
            Report.STATUS_VERIFIED,
            Report.STATUS_IN_PROGRESS,
            Report.STATUS_RESOLVED,
        ]

        reports_to_create = []
        amount_to_add = target_count - current_count
        now = timezone.now()

        for index in range(amount_to_add):
            category = random.choice(categories)
            location = random.choice(locations)
            reporter_name = random.choice(names)
            title = random.choice(title_templates).format(
                category=category,
                location=location,
            )
            description = random.choice(description_templates).format(
                category_lower=category.lower(),
                location=location,
            )
            created_at = now - timedelta(
                days=random.randint(0, 180),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            reports_to_create.append(
                Report(
                    reporter_name=reporter_name,
                    title=f"{title} #{current_count + index + 1}",
                    category=category,
                    description=description,
                    location=location,
                    status=random.choice(statuses),
                    created_at=created_at,
                )
            )

        Report.objects.bulk_create(reports_to_create, batch_size=200)

        self.stdout.write(
            self.style.SUCCESS(
                f"Berhasil menambahkan {amount_to_add} data dummy. Total laporan sekarang {Report.objects.count()}."
            )
        )
