

## Deploy site dev
```bash
ssh -t user_name@ip 'bash ./deploy-dev.sh'
ssh -t user_name@ip 'bash ./upgrade-module-dev.sh "custom_hr,custom_web"'
```

## Deploy site test

```bash
ssh -t user_name@ip 'bash ./deploy.sh'
ssh -t user_name@ip 'bash ./upgrade-module.sh "custom_hr,custom_web"'
```

# Replace custom_hr,custom_web with module list you need to upgrade
# Add database name after moulde list to choose which db will be updated


