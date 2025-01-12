import graphene
from graphene_django.types import DjangoObjectType
from .models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None
    
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
    
    post = graphene.Field(PostType)

    def mutate(self, info, title, content):
        post = Post(title=title, content=content)
        post.save()
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, content=None):
        post = Post.objects.get(pk=id)
        if title is not None:
            post.title = title
        if content is not None:
            post.content =content
        post.save()
        return UpdatePost(post=post)
    
class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()

    def mutate(self, info, id):
        post = Post.objects.get(pk=id)
        post.delete()
        return DeletePost(success=True)
    
class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
        
schema = graphene.Schema(query=Query, mutation=Mutation)