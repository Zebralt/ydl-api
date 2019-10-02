

// var REMOTE = 'http://localhost:8080/download';
var REMOTE = 'http://ydlapi_default:8080/download';


GET = (url) => {
    return fetch(
        url, {
            mode: 'cors'
        }
    )
}

POST = (url, body) => {
    return fetch(
        url, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(body)
        }
    )
}

on_enter = (event, fn, target) => {
    if (event.code == 'Enter' || event.code == 'NumpadEnter') {
        fn(target);
    }
}

process_input = elm => {

    if (!elm.value.trim()) {
        return;
    }

    POST(`${REMOTE}`, {
        'url': elm.value
    }).then(
        (response) => {
            return response.json();
        }
    ).then(
        (json) => {
            console.log(json);
            register_task(json);
        }
    )
}

register_task = (task_id) => {

    li_obj = document.createElement('li');
    document.querySelector('#history').children[0].appendChild(li_obj);

    task = {
        dom_obj: li_obj,
        id: task_id,
        counter: 10,
        status: 0
    }

    render_task(task);

    // Query task metadata, check if status is success, if not, wait then retry
    update_task_status(task);
    // until status is success
}

render_task = task => {

    cls = '';
    status = '';

    switch (task.status) {
        case 0:
            cls = 'pending';
            status = 'Pending';
            break;
        case 1:
            cls = 'success';
            status = 'Success';
            break;
        case 2:
            cls = 'failure';
            status = 'Failed;'
            break;
        default: 
            status = '?';
        break;
    }

    task.dom_obj.className = cls;

    task.dom_obj.innerHTML = `
    <span> ${task.id} </span>
    <span> ${status} </span>
    `;

}

update_task_status = task => {

    console.log(`Updating ${task.id}`)

    GET(`${REMOTE}/task/${task.id}`).then(
        response => {
            return response.json();
        }
    ).then(
        json => {
            console.log(json);
            if (json.status != 1) {
                task.counter -= 1;
            }
            else {
                task.counter = -1;
            }

            if (task.counter == 0) {
                json.status = 2;
            }

            task.status = json.status;

            render_task(task);

            if (task.counter > 0) {
                setTimeout(() => {
                    update_task_status(task);
                }, 1000)
            }
        }
    )

}
