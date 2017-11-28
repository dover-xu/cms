from focus.models import MyUser, Note, Comment, Praise, Share, Tread
from rest_framework import serializers
from focus.views import MyUser


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    # notes = serializers.HyperlinkedRelatedField(many=True, view_name='note-detail', read_only=True)
    # avatar = serializers.ImageField()

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'sex', 'profile', 'email', 'avatar')


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    user = MyUserSerializer(read_only=True)
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)
    pub_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Note
        fields = (
            'id', 'text', 'image', 'hot', 'click_num', 'recmd', 'user', 'category', 'comments',
            'comment_str', 'praise_str', 'tread_str', 'share_str', 'pub_date')

    def create(self, validated_data):
        """响应 POST 请求
        :param validated_data:
        """
        # 自动为用户提交的 model 添加 owner
        validated_data['user'] = self.context['request'].user
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """响应 PUT 请求
        :param instance:
        :param validated_data:
        """
        instance.text = validated_data.get('text', instance.text)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    # note = serializers.ReadOnlyField(source='note.id')
    # user = serializers.ReadOnlyField(source='user.username')
    user = MyUserSerializer(read_only=True)
    pub_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Comment
        fields = (
            'text', 'id', 'user', 'pub_date'
        )


class PraiseSerializer(serializers.HyperlinkedModelSerializer):
    # note = serializers.ReadOnlyField(source='note.id')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Praise
        fields = (
            'user', 'id', 'note', 'praise_date'
        )


class TreadSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Tread
        fields = (
            'user', 'id', 'note', 'tread_date'
        )


class ShareSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Share
        fields = (
            'user', 'id', 'note', 'share_date'
        )
