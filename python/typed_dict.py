import typing as t
import typing_extensions as te


class TD(te.TypedDict):
    """
    An artifact from a computation that can be serialized or deserialized
    """

    #: The computed artifact, which may be of any type
    artifact: t.Any = None

    #: A file_id is a key used to identify the file in the ``ArtifactStore``
    file_id: t.Optional[str] = None

    #: The ``info`` dictionary is passed into ``ArtifactStore.create_artifact()``
    info: t.Optional[t.Dict] = None

    #: The Python ``id()`` of the artifact
    object_id: int = 0

    #: The name of the finalization method on the artifact to call before saving
    save_method: t.Optional[str] = None

    #: The name of the serializer
    serializer: str = 'pickle'

    #: The sha1 hash of the artifact
    sha1: str = ''


print(TD())
