from django.core.management.base import BaseCommand

from recommendations.models import Track


TRACKS = [
    # Rock
    ("track_001", "Yellow", "Coldplay", "rock", "happy", 92),
    ("track_002", "Fix You", "Coldplay", "rock", "emotional", 95),
    ("track_003", "Paradise", "Coldplay", "rock", "happy", 90),
    ("track_004", "Viva La Vida", "Coldplay", "rock", "energetic", 94),
    ("track_005", "Believer", "Imagine Dragons", "rock", "energetic", 96),
    ("track_006", "Demons", "Imagine Dragons", "rock", "sad", 93),
    ("track_007", "Radioactive", "Imagine Dragons", "rock", "energetic", 91),
    ("track_008", "Whatever It Takes", "Imagine Dragons", "rock", "motivational", 89),
    ("track_009", "Numb", "Linkin Park", "rock", "angry", 97),
    ("track_010", "In The End", "Linkin Park", "rock", "emotional", 98),

    # Pop
    ("track_011", "Hello", "Adele", "pop", "sad", 97),
    ("track_012", "Rolling in the Deep", "Adele", "pop", "energetic", 96),
    ("track_013", "Someone Like You", "Adele", "pop", "sad", 95),
    ("track_014", "Easy On Me", "Adele", "pop", "emotional", 94),
    ("track_015", "Perfect", "Ed Sheeran", "pop", "romantic", 96),
    ("track_016", "Shape of You", "Ed Sheeran", "pop", "happy", 98),
    ("track_017", "Photograph", "Ed Sheeran", "pop", "romantic", 91),
    ("track_018", "Thinking Out Loud", "Ed Sheeran", "pop", "romantic", 93),
    ("track_019", "Blinding Lights", "The Weeknd", "pop", "energetic", 99),
    ("track_020", "Save Your Tears", "The Weeknd", "pop", "emotional", 95),

    # Bollywood
    ("track_021", "Kesariya", "Arijit Singh", "bollywood", "romantic", 98),
    ("track_022", "Tum Hi Ho", "Arijit Singh", "bollywood", "romantic", 99),
    ("track_023", "Channa Mereya", "Arijit Singh", "bollywood", "sad", 97),
    ("track_024", "Agar Tum Saath Ho", "Alka Yagnik", "bollywood", "sad", 96),
    ("track_025", "Apna Bana Le", "Arijit Singh", "bollywood", "romantic", 94),
    ("track_026", "Tera Ban Jaunga", "Akhil Sachdeva", "bollywood", "romantic", 92),
    ("track_027", "Ilahi", "Arijit Singh", "bollywood", "happy", 95),
    ("track_028", "Zinda", "Siddharth Mahadevan", "bollywood", "motivational", 90),
    ("track_029", "Kar Har Maidaan Fateh", "Sukhwinder Singh", "bollywood", "motivational", 93),
    ("track_030", "Galliyan", "Ankit Tiwari", "bollywood", "emotional", 91),

    # Hip-Hop
    ("track_031", "Lose Yourself", "Eminem", "hip-hop", "motivational", 99),
    ("track_032", "Without Me", "Eminem", "hip-hop", "energetic", 96),
    ("track_033", "Mockingbird", "Eminem", "hip-hop", "emotional", 95),
    ("track_034", "God's Plan", "Drake", "hip-hop", "confident", 97),
    ("track_035", "Hotline Bling", "Drake", "hip-hop", "relaxed", 94),
    ("track_036", "One Dance", "Drake", "hip-hop", "happy", 96),
    ("track_037", "HUMBLE.", "Kendrick Lamar", "hip-hop", "confident", 95),
    ("track_038", "DNA.", "Kendrick Lamar", "hip-hop", "energetic", 93),

    # Electronic
    ("track_039", "Faded", "Alan Walker", "electronic", "sad", 98),
    ("track_040", "Alone", "Alan Walker", "electronic", "emotional", 96),
    ("track_041", "The Spectre", "Alan Walker", "electronic", "energetic", 94),
    ("track_042", "Titanium", "David Guetta", "electronic", "motivational", 97),
    ("track_043", "Memories", "David Guetta", "electronic", "emotional", 92),
    ("track_044", "Animals", "Martin Garrix", "electronic", "energetic", 96),

    # Classical
    ("track_045", "Clair de Lune", "Claude Debussy", "classical", "relaxed", 90),
    ("track_046", "Moonlight Sonata", "Beethoven", "classical", "emotional", 94),
    ("track_047", "Für Elise", "Beethoven", "classical", "relaxed", 95),
    ("track_048", "Canon in D", "Pachelbel", "classical", "peaceful", 93),
    ("track_049", "Spring", "Vivaldi", "classical", "happy", 91),
    ("track_050", "The Four Seasons", "Vivaldi", "classical", "energetic", 89),
]


class Command(BaseCommand):
    help = "Seed the database with sample music tracks."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for track in TRACKS:
            spotify_id, name, artist, genre, mood, popularity = track

            _, created = Track.objects.get_or_create(
                spotify_id=spotify_id,
                defaults={
                    "name": name,
                    "artist_name": artist,
                    "genre": genre,
                    "mood": mood,
                    "popularity": popularity,
                },
            )

            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created: {created_count}, Skipped: {skipped_count}"
            )
        )