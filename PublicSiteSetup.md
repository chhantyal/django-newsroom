# Setup #

## Get virtualenv ##
```
# if not installed
easy_install virtualenv

mkdir public.news21.com

cd public.news21.com

virtualenv public-env

source public-env/bin/activate

cd public-env
```

## Get pip ##

```
easy_install pip
```


## Get Django ##

```
pip install django
```


## Get firepython ##
```
easy_install firepython
```

## Get django-debug-toolbar ##
```
easy_install django-debug-toolbar
```

## Get Dmigrations ##
```
svn checkout http://dmigrations.googlecode.com/svn/trunk/ dmigrations-read-only
cd dmigrations-read-only
python setup.py install
cd ../
rm -rf dmigrations-read-only
```

## Get jsonpickle ##
```
pip install jsonpickle
```

## Get django-base ##

cd into the root of the public.news21.com directory
```
git clone git://github.com/jonatkinson/django-base.git
cp -r django-base public-site
```


# Get started #

Edit your settings.py
etc.