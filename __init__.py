from os.path import join, dirname

from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_utils.parse import fuzzy_match
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search, ocp_featured_media
from youtube_archivist import IAArchivist


class ClassicScifiHorrorSkill(OVOSCommonPlaybackSkill):

    def __init__(self):
        super().__init__("ClassicScifiHorror")
        self.supported_media = [MediaType.MOVIE, MediaType.GENERIC]
        self.skill_icon = join(dirname(__file__), "ui", "scifihorror.png")
        self.archive = IAArchivist("SciFi_Horror")

    def initialize(self):
        if len(self.archive.db) == 0:
            # no database, download from url TODO
            self.archive.archive_collection("SciFi_Horror")

    def normalize_title(self, title):
        title = title.lower().strip()
        title = self.remove_voc(title, "movie")
        title = self.remove_voc(title, "play")
        title = self.remove_voc(title, "video")
        title = self.remove_voc(title, "scifi")
        title = self.remove_voc(title, "horror")
        title = title.replace("|", "").replace('"', "") \
            .replace(':', "").replace('”', "").replace('“', "") \
            .strip()
        return " ".join(
            [w for w in title.split(" ") if w])  # remove extra spaces

    def match_skill(self, phrase, media_type):
        score = 0
        if self.voc_match(phrase, "movie") or media_type == MediaType.MOVIE:
            score += 10
        if self.voc_match(phrase, "old"):
            score += 30
        if self.voc_match(phrase, "public_domain"):
            score += 15
        if self.voc_match(phrase, "scifi"):
            score += 30
        if self.voc_match(phrase, "horror"):
            score += 30
        return score

    def calc_score(self, phrase, match, base_score=0):
        score = base_score
        score += 100 * fuzzy_match(phrase.lower(), match["title"].lower())
        return min(100, score)

    @staticmethod
    def entry2mediatype(video):
        if video.get("sound", "") == "silent":
            m = MediaType.SILENT_MOVIE
        elif video.get("color", "color") != "color":
            m = MediaType.BLACK_WHITE_MOVIE
        else:
            m = MediaType.MOVIE
        return m

    def get_playlist(self, score=50):
        pl = [{
            "title": video["title"],
            "image": self.skill_icon,
            "match_confidence": 70,
            "media_type": self.entry2mediatype(video),
            "uri": video["streams"][0],  # TODO format selection
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "skill_id": self.skill_id
        } for _, video in self.archive.db.items() if video.get("streams")]
        return {
            "match_confidence": score,
            "media_type": MediaType.MOVIE,
            "playlist": pl,
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "image": self.skill_icon,
            "skill_id": self.skill_id,
            "title": "Classic Scifi/Horror (Movie Playlist)",
            "author": "Internet Archive"
        }

    @ocp_search()
    def search_db(self, phrase, media_type):
        base_score = self.match_skill(phrase, media_type)
        if self.voc_match(phrase, "horror"):
            yield self.get_playlist(base_score)
        if media_type == MediaType.MOVIE:
            # only search db if user explicitly requested movies
            phrase = self.normalize_title(phrase)
            for _, video in self.archive.db.items():
                yield {
                    "title": video["title"],
                    "image": self.skill_icon,
                    "match_confidence": self.calc_score(phrase, video, base_score),
                    "media_type": self.entry2mediatype(video),
                    "uri": video["streams"][0],  # TODO format selection
                    "playback": PlaybackType.VIDEO,
                    "skill_icon": self.skill_icon,
                    "skill_id": self.skill_id
                }

    @ocp_featured_media()
    def featured_media(self):
        return self.get_playlist()['playlist']


def create_skill():
    return ClassicScifiHorrorSkill()
