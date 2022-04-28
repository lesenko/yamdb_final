from django.db.models import Avg
from django.http import Http404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating_from_review')
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')
        read_only_fields = ('id', )

    def get_rating_from_review(self, obj):
        score_avg = obj.reviews.aggregate(Avg('score'))['score__avg']
        if score_avg is not None:
            return int(score_avg)
        return None


class TitleSerializerCreate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        if (self.context['request'].method == 'POST'):
            title_id = self.context['view'].kwargs.get('title_id')
            user = self.context['request'].user
            if Review.objects.filter(
                author=user,
                title_id=title_id
            ).exists():
                raise serializers.ValidationError("400 Bad Request")
        return data

    class Meta:
        fields = 'id', 'text', 'author', 'score', 'pub_date'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        review_id = self.context['view'].kwargs.get('review_id')
        if Review.objects.filter(
            id=review_id,
            title_id=title_id
        ).exists():
            return data
        raise Http404

    class Meta:
        fields = 'id', 'text', 'author', 'pub_date'
        model = Comment
