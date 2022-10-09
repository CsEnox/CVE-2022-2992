#!/usr/bin/env bash
container_name=$1
shift
timeout=$1

default_timeout=120

if [ -z ${timeout} ]; then
    timeout=${default_timeout}
fi

RETURN_HEALTHY=0
RETURN_STARTING=1
RETURN_UNHEALTHY=2
RETURN_UNKNOWN=3
RETURN_ERROR=99

function usage() {
    echo "
    Usage: wait-for-healthy-container.sh <container name> [timeout]
    "
    return
}

function get_health_state {
    state=$(docker inspect -f '{{ .State.Health.Status }}' ${container_name})
    return_code=$?
    if [ ! ${return_code} -eq 0 ]; then
        exit ${RETURN_ERROR}
    fi
    if [[ "${state}" == "healthy" ]]; then
        return ${RETURN_HEALTHY}
    elif [[ "${state}" == "unhealthy" ]]; then
        return ${RETURN_UNHEALTHY}
    elif [[ "${state}" == "starting" ]]; then
        return ${RETURN_STARTING}
    else
        return ${RETURN_UNKNOWN}
    fi
}

function wait_for() {
    echo "Wait for container '$container_name' to be healthy for max $timeout seconds..."
    for i in `seq ${timeout}`; do
        get_health_state
        state=$?
        if [ ${state} -eq 0 ]; then
            echo "Container is healthy after ${i} seconds."
            exit 0
        fi
        sleep 1
    done

    echo "Timeout exceeded. Health status returned: $(docker inspect -f '{{ .State.Health.Status }}' ${container_name})"
    exit 1
}

if [ -z ${container_name} ]; then
    usage
    exit 1
else
    wait_for
fi
