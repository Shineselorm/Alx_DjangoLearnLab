# Tagging and Search

## Tagging
- Posts can have multiple tags; enter tags as comma-separated values in the Post form (create/edit).
- Tags are created on the fly if they don't exist.
- On the post detail page, tags are displayed and link to a filtered list.

## URLs
- View posts by tag: `/tags/<tag_name>/`
- Search: `/search/?q=keyword`

## Search
- Searches `title`, `content`, and tag names.
- Accessible via the search bar in the top navigation.

## How to Test
1. Create/edit a post with tags like: `django, web, tutorial`.
2. Click a tag on the post detail page to see filtered posts.
3. Use the search bar (e.g., `django`) and verify results include matching titles, content, or tags.
