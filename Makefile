_today =`date '+%Y-%m-%d_%H:%M:%S'`
_commit_name = "autocommit_$(_today)"
app_name = y_eda_tg_bot
_path = $(CURDIR)

_common-service-path = /etc/systemd/system/

copy-service:
	@echo "⚙️  moving service to $(_common-service-path)\n"
	@sudo cp $(_path)/service/$(app_name).service $(_common-service-path)/$(app_name).service
	@echo "⚙️  managing service\n"
	-@sudo systemctl enable $(app_name)
	-@sudo systemctl daemon-reload

start-service:
	-@sudo systemctl start $(app_name).service
	@echo "\n ✅  started "

status-service:
	-@sudo systemctl status $(app_name).service

cat-service:
	@systemctl cat $(app_name)

cat-log:
	@journalctl --unit=$(app_name)

