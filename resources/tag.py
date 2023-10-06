from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        ).first():
            abort(400, message="Tag with that name already exists.")

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="delete a tag if no item is tagged with it",
        example={"message": "tag deleted"},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="returned if the tag is assigned to one or more items. In this case, the tag is not deleted",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag Deleted"}
        abort(
            400,
            message="Could not delete tag. Make sure Tag is not assosciated with any items, then try again.",
        )


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        # if ItemModel.query.filter(
        #     ItemModel.id != item_id, TagModel.id != tag_id
        # ).first():
        #     abort(400, message="Tag with that name already exists.")
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An Error occurred while inserting the tag")

        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def deletet(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An Error occurred while inserting the tag")

        return {"message": "Item removed from tag", "item": item, "tag": tag}
