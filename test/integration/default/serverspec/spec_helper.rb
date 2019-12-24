require 'serverspec'

# :backend can be either :exec or :ssh
# since we are running local we use :exec
set :backend, :exec