-- parent = models.ForeignKey('self', verbose_name='Категория', blank=True, null=True, editable=False)
-- title = models.CharField('Заголовок', max_length=255)
-- slug_title = models.SlugField('Имя для ссылки', unique=True)
-- preview = models.CharField('Краткое описание', max_length=2550)
-- content = models.TextField('Описание', blank=True, null=True)
-- contentSEO = models.TextField('Описание для SEO', blank=True, null=True)
-- image = models.ImageField('Изображение', upload_to=path_for_object, blank=True, null=True)
-- show = models.BooleanField('Показывать', default=True)
-- themes = models.ManyToManyField(Theme, verbose_name=u"Темы спецпредложений", blank=True, null=True,
--                                 related_name="themes_cat")
-- title_seo = models.CharField('Заголовок для SEO', max_length=255, blank=True, null=True)
-- metakey = models.CharField('Meta key', max_length=255, blank=True, null=True)
-- metades = models.CharField('Meta des', max_length=255, blank=True, null=True)



USE sklad_new2;



DROP PROCEDURE IF EXISTS catalog_migrate;
CREATE PROCEDURE catalog_migrate()
BEGIN

    INSERT INTO sklad_new2.catalog_category
    (id,
     path,
     depth,
     numchild,
     parent_id,
     image,
     uri)
    SELECT id,
     path,
     depth,
     numchild,
     parent_id,
     image,
     slug_title
    FROM sklad.catalog_category;



END;


# catalog_category,"CREATE TABLE `catalog_category` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `path` varchar(255) NOT NULL,
#   `depth` int(10) unsigned NOT NULL,
#   `numchild` int(10) unsigned NOT NULL DEFAULT '0',
#   `parent_id` int(11) DEFAULT NULL,
#   `title` varchar(255) NOT NULL,
#   `slug_title` varchar(50) NOT NULL,
#   `image` varchar(100) DEFAULT NULL,
#   `show` tinyint(1) NOT NULL DEFAULT '1',
#   `title_seo` varchar(255) DEFAULT NULL,
#   `metakey` varchar(255) DEFAULT NULL,
#   `metades` varchar(255) DEFAULT NULL,
#   `preview` varchar(2550) NOT NULL,
#   `content` longtext,
#   `contentSEO` longtext,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `path` (`path`),
#   UNIQUE KEY `slug_title` (`slug_title`),
#   KEY `catalog_category_63f17a16` (`parent_id`)
# ) ENGINE=MyISAM AUTO_INCREMENT=520 DEFAULT CHARSET=cp1251"
#
#
# catalog_category,"CREATE TABLE `catalog_category` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `path` varchar(255) NOT NULL,
#   `depth` int(10) unsigned NOT NULL,
#   `numchild` int(10) unsigned NOT NULL,
#   `parent_id` int(11) DEFAULT NULL,
#   `name` varchar(255) NOT NULL,
#   `show` tinyint(1) NOT NULL,
#   `image` varchar(100) DEFAULT NULL,
#   `uri` varchar(255) NOT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `path` (`path`),
#   KEY `catalog_category_410d0aac` (`parent_id`)
# ) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8"



TRUNCATE sklad_new2.catalog_category;