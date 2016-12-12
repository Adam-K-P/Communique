LAMBDA_FUNCS = receive_text add_email add_phone add_post delete_post edit_post get_phone_numbers get_posts

LAMBDA_CLEANERS = clean_receive_text clean_add_email clean_add_phone clean_add_post clean_delete_post clean_edit_post clean_get_phone_numbers clean_get_posts

.PHONY: $(LAMBDA_FUNCS) $(LAMBDA_CLEANERS)

all: $(LAMBDA_FUNCS)

receive_text: receive_text/receive_text.py
	cd receive_text && zip receive_text *

add_email: add_email/add_email.py
	cd add_email && zip add_email *

add_phone: add_phone/add_phone.py
	cd add_phone && zip add_phone *

add_post: add_post/add_post.py
	cd add_post && zip add_post *

delete_post: delete_post/delete_post.py
	cd delete_post && zip delete_post *

edit_post: edit_post/edit_post.py
	cd edit_post && zip edit_post *

get_phone_numbers: get_phone_numbers/get_phone_numbers.py
	cd get_phone_numbers && zip get_phone_numbers *

get_posts: get_posts/get_posts.py
	cd get_posts && zip get_posts *

clean: $(LAMBDA_CLEANERS)

clean_receive_text:
	cd receive_text && rm -f *.zip

clean_add_email:
	cd add_email && rm -f *.zip

clean_add_phone:
	cd add_phone && rm -f *.zip

clean_add_post:
	cd add_post && rm -f *.zip

clean_delete_post:
	cd delete_post && rm -f *.zip

clean_edit_post:
	cd edit_post && rm -f *.zip

clean_get_phone_numbers:
	cd get_phone_numbers && rm -f *.zip

clean_get_posts:
	cd get_posts && rm -f *.zip

