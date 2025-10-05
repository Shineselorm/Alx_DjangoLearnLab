# Post Management (CRUD)

This document explains how to use the Post CRUD features.

## URLs
- `/posts/` – List all posts
- `/posts/new/` – Create a new post (login required)
- `/posts/<id>/` – View post details
- `/posts/<id>/edit/` – Edit post (author only)
- `/posts/<id>/delete/` – Delete post (author only)

## Views (class-based)
- `PostListView` – lists posts, newest first
- `PostDetailView` – shows a single post
- `PostCreateView` – creates a post; sets `author=request.user`
- `PostUpdateView` – edit; restricted to author
- `PostDeleteView` – delete; restricted to author

## Forms
- `PostForm` – fields: title, content

## Templates
- `blog/templates/blog/post_list.html`
- `blog/templates/blog/post_detail.html`
- `blog/templates/blog/post_form.html`
- `blog/templates/blog/post_confirm_delete.html`

## Permissions
- Create: `LoginRequiredMixin`
- Update/Delete: `LoginRequiredMixin` + `UserPassesTestMixin` (author-only)

## Testing
1. Create a user and login.
2. Create a post via `/posts/new/`.
3. Verify it appears on `/posts/` and details at `/posts/<id>/`.
4. Edit and delete as the author.
