from graphene import ObjectType, String, Boolean, ID, List, Field, Int, Date


class Podcast(ObjectType):
    author = String()
    categories = List(String)
    description = String()
    id = String()
    language = String()
    sort_order = Int()
    subscribed = String()
    thumbnail_url_large = String()
    thumbnail_url_medium = String()
    thumbnail_url_small = String()
    thumbnail_url_src = String()
    title = String()
    url = String()
    uuid = String()


class Episode(ObjectType):
    duration = Int()
    file_type = String()
    id = ID()
    is_deleted: Boolean()
    is_video: Boolean()
    played_up_to = Int()
    playing_status = Int()
    published_at = Date()
    size = String()
    starred = Boolean()
    title = String()
    url = String()
    uuid = ID()
    podcast = Field(Podcast)
