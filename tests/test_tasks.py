from pathlib import Path

from elm_doc import tasks


def test_create_tasks_only_elm_stuff(tmpdir, elm_version, make_elm_project):
    make_elm_project(elm_version, tmpdir, copy_elm_stuff=True)
    output_dir = tmpdir.join('docs')
    with tmpdir.as_cwd():
        result = list(tasks.create_tasks(Path('.'), Path(str(output_dir))))
        expected_task_names = [
            'build_project_docs_json',
            'project_page',
            'project_latest_link',
            'download_project_docs_json',
            'project_readme',
            'module_page',
            'index',
            'all_packages',
            'new_packages',
            'assets']
        assert basenames_in_first_seen_order(result) == expected_task_names


def test_create_tasks_only_project_modules(
        tmpdir, overlayer, elm_version, make_elm_project):
    modules = ['Main.elm']
    make_elm_project(elm_version, tmpdir, modules=modules)
    output_dir = tmpdir.join('docs')
    with tmpdir.as_cwd():
        tmpdir.join('README.md').write('hello')
        result = list(tasks.create_tasks(Path('.'), Path(str(output_dir))))

        expected_task_names = [
            'build_project_docs_json',
            'project_page',
            'project_readme',
            'project_latest_link',
            'module_page',
            'index',
            'all_packages',
            'new_packages',
            'assets']
        assert basenames_in_first_seen_order(result) == expected_task_names


def test_create_tasks_for_validation(tmpdir, elm_version, make_elm_project):
    make_elm_project(elm_version, tmpdir)
    output_dir = tmpdir.join('docs')
    with tmpdir.as_cwd():
        result = list(tasks.create_tasks(Path('.'), Path(str(output_dir)), validate=True))

        expected_task_names = [
            'validate_project_docs_json',
            ]
        assert basenames_in_first_seen_order(result) == expected_task_names


def basenames_in_first_seen_order(tasks):
    rv = []
    seen = set()
    for task in tasks:
        basename = task['basename'].split(':')[0]
        if basename not in seen:
            seen.add(basename)
            rv.append(basename)
    return rv
