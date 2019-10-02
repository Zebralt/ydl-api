
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
    if (event.code == 'Enter') {
        fn(target);
    }
}

process_input = elm => {

    if (!elm.value.trim()) {
        return;
    }

    POST('http://localhost:8080/download', {
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
        status: 'Pending'
    }

    render_task(task);

    // Query task metadata, check if status is success, if not, wait then retry
    update_task_status(task);
    // until status is success
}

render_task = task => {

    task.dom_obj.innerHTML = `
    <span> ${task.id} </span>
    <span> ${task.status} </span>
    `;

    cls = '';

    switch (task.status) {
        case 'Pending':
            cls = 'pending';
            break;
        case 'Success':
            cls = 'success';
            break;
        case 'Failed':
            cls = 'failure';
            break;
        default: break;
    }

    task.dom_obj.className = cls;

}

update_task_status = task => {

    console.log(`Updating ${task.id}`)

    GET(`http://localhost:8080/task/${task.id}`).then(
        response => {
            return response.json();
        }
    ).then(
        json => {
            console.log(json);
            if (json.status != 'Success') {
                task.counter -= 1;
            }
            else {
                task.counter = -1;
            }

            if (task.counter == 0) {
                json.status = 'Failed'
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
