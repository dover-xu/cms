from focus.models import MyUser, Note, Comment, Praise, Share, Tread
from rest_framework import serializers
from focus.views import MyUser


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    notes = serializers.HyperlinkedRelatedField(many=True, view_name='note-detail', read_only=True)

    class Meta:
        model = MyUser
        fields = ('url', 'id', 'username', 'email', 'notes')


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)

    class Meta:
        model = Note
        fields = (
            'url', 'id', 'text', 'hot', 'click_num', 'recommend', 'user', 'category', 'comments', 'comment_num',
            'praise_num', 'tread_num', 'share_num', 'pub_date')

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
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = (
            'text', 'user', 'note', 'pub_date'
        )


class PraiseSerializer(serializers.HyperlinkedModelSerializer):
    # note = serializers.ReadOnlyField(source='note.id')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Praise
        fields = (
            'user', 'note', 'praise_date'
        )


class TreadSerializer(serializers.HyperlinkedModelSerializer):
    # note = serializers.ReadOnlyField(source='note.id')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Tread
        fields = (
            'user', 'note', 'tread_date'
        )


class ShareSerializer(serializers.HyperlinkedModelSerializer):
    note = serializers.ReadOnlyField(source='note.id')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Share
        fields = (
            'user', 'note', 'share_date'
        )
