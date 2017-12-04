import coreapi
import coreschema
from rest_framework.schemas import ManualSchema, AutoSchema

# ---------focus schema-------------

contentsSchema = ManualSchema(
        description="""获取浏览页帖子\n
        type: integer (0：用户发表的帖子, 1：用户分享的帖子, 2：用户评论的帖子)
        sort: integer (0：推荐列表，1：最新列表，2：最热列表)
        current: integer (当前页码)
        display: integer (每页显示条数)
        """,
        fields=[
            coreapi.Field("type", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("sort", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("current", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("display", required=True, location="form", schema=coreschema.Integer())
        ])

detailsSchema = ManualSchema(
        description=
        """获取用户中心内容\n
        type: integer(0：用户发表的帖子, 1：用户分享的帖子, 2：用户评论的帖子)
        current: integer()
        """,
        fields=[
            coreapi.Field("type", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("current", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("display", required=True, location="form", schema=coreschema.Integer())
        ])

ucenterSchema = ManualSchema(
        description="""获取用户中心内容\n
        type: integer (0：用户发表的帖子, 1：用户分享的帖子, 2：用户评论的帖子)
        current: integer (当前页码)
        display: integer (每页显示条数)
        """,
        fields=[
            coreapi.Field("type", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("current", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("display", required=True, location="form", schema=coreschema.Integer())
        ])

delNoteOrCommentSchema = ManualSchema(
        description="""删帖或者删评论\n
        note_id: integer (帖子ID)
        comment_id: integer (评论ID)
        """,
        fields=[
            coreapi.Field("note_id", required=False, location="form", schema=coreschema.Integer()),
            coreapi.Field("comment_id", required=False, location="form", schema=coreschema.Integer())
        ])

# TODO (dong): swagger can not upload file
publishSchema = ManualSchema(
        description="""发帖
        """,
        fields=[
        ])

addCommentSchema = ManualSchema(
        description="""发表评论\n
        note_id: integer (帖子ID)
        text: string (评论内容)
        """,
        fields=[
            coreapi.Field("note_id", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("text", required=True, location="form", schema=coreschema.String())
        ])

addPraiseTreadShareSchema = ManualSchema(
        description="""添加赞/踩/分享\n
        note_id: integer (帖子ID)
        action: string (请求类型: 'praise'/'tread'/'share')
        """,
        fields=[
            coreapi.Field("note_id", required=True, location="form", schema=coreschema.Integer()),
            coreapi.Field("action", required=True, location="form", schema=coreschema.String())
        ])

# ---------manager schema-------------

loginSchema = ManualSchema(
        description="""登录请求\n
        username: string (用户昵称)
        password: string (用户密码)
        """,
        fields=[
            coreapi.Field("username", required=True, location="form", schema=coreschema.String()),
            coreapi.Field("password", required=True, location="form", schema=coreschema.String())
        ])

signupSchema = ManualSchema(
        description="""注册请求\n
        username: string (用户昵称)
        password1: string (用户密码)
        password2: string (用户密码确认)
        """,
        fields=[
            coreapi.Field("username", required=True, location="form", schema=coreschema.String()),
            coreapi.Field("password1", required=True, location="form", schema=coreschema.String()),
            coreapi.Field("password2", required=True, location="form", schema=coreschema.String())
        ])