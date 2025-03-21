pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'lab_5'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/drawing-area.blp',
    'gtk/shape-picker.blp',
    'gtk/help-overlay.blp',
    'gtk/window.blp',
    'gtk/table.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('lab-5',
  'lab-5.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'lab-5.in',
  output: 'lab-5',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

lab_5_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'drawing_area.py',
  'shapes.py',
  'shape_picker.py',
  'singleton.py',
  'table.py',
]

install_data(lab_5_sources, install_dir: moduledir)
