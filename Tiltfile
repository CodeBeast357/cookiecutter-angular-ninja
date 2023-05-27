load('ext://uibutton', 'cmd_button', 'location', 'text_input')


###################################
#
#  Ingress Controller
load('./tilt_utils/install_ingress_controller.tilt', 'install_ingress_controller')
install_ingress_controller()




local_resource('postgres-databases', cmd='kubectl exec -it `kubectl get pods | grep postgres | grep Running` -- psql -U postgres -c "\\l"', labels=['postgres'], allow_parallel=True, auto_init=False)
local_resource('postgres-tables', cmd='kubectl exec -it `kubectl get pods | grep postgres | grep Running` -- psql -U postgres -c "\\dt" ad_hoc_analytics_database', labels=['postgres'], allow_parallel=True, auto_init=False)

# AD_HOC_ENVIRONMENT=jupyter ./manage.py shell_plus --lab

# For troubleshooting or copy/pasta of migrations: 

# kubectl exec -it `kubectl get pods | grep ad-hoc | grep api | grep Running` -- bash
# kubectl exec -it `kubectl get pods | grep ad-hoc | grep ui | grep Running` -- bash

docker_build('ad-hoc-analytics-api-image', 'generic_api/', 
    live_update=[
        sync('./generic_api/generic/', '/usr/src/generic/generic/'),
        run(
            'pip install -r /usr/src/requirements.txt',
            trigger=['./generic_api/requirements.txt']
        )
    ]
)
docker_build('ad-hoc-analytics-ui-image', 
    context='generic_ui/generic_app',
    dockerfile='generic_ui/generic_app/Dockerfile-dev',
    live_update=[
        # Sync files from host to container
        sync('generic_ui/generic_app/src', '/usr/src/app/src/'),
        sync('generic_ui/generic_app/package.json', '/usr/src/app/'),
        sync('generic_ui/generic_app/package-lock.json', '/usr/src/app/'),
    ]
)
docker_prune_settings( disable = False , max_age_mins = 360 , num_builds = 0 , interval_hrs = 1 , keep_recent = 2 ) 

k8s_yaml([
    'generic_api/k8s/deployment.yaml',
    # 'generic_api/k8s/hpa.yaml',
    'generic_api/k8s/service.yaml',
    'generic_api/k8s/ingress.yaml',
])
k8s_yaml([
    'generic_ui/k8s/deployment.yaml',
    # 'generic_ui/k8s/hpa.yaml',
    'generic_ui/k8s/service.yaml',
    'generic_ui/k8s/ingress.yaml',
])
k8s_yaml('storage-class.yaml')
k8s_yaml([
    'postgres-server/secrets.yaml',
    'postgres-server/deployment.yaml',
    'postgres-server/service.yaml',
    'postgres-server/ingress.yaml',
    'postgres-server/volume-claim.yaml',
    'postgres-server/volume.yaml',
])
k8s_yaml([
    'rabbitmq/secrets.yaml',
    'rabbitmq/deployment.yaml',
    'rabbitmq/service.yaml',
    'rabbitmq/ingress.yaml',
    # 'rabbitmq/volume-claim.yaml',
    # 'rabbitmq/volume.yaml',
])


#k8s_resource('generic-ui', port_forwards=8080, labels=['services'])
k8s_resource('ad-hoc-analytics-ui', labels=['UI'])
k8s_resource('ad-hoc-analytics-api', labels=['API'])
k8s_resource('ad-hoc-analytics-worker', labels=['API'])
k8s_resource('postgres', labels=['postgres'])
k8s_resource('rabbitmq', labels=['rabbitmq'])

cmd_button(
    name='nav-black',
    argv=['black', 'generic_api/generic_api/'],
    text='Python Black',
    location=location.NAV,
    icon_name='install_desktop'
)
