mkdir qgis_easy_query
mkdir qgis_easy_query\i18n
xcopy *.py qgis_easy_query
xcopy *.ui qgis_easy_query
xcopy *.png qgis_easy_query
xcopy README.md qgis_easy_query
xcopy LICENSE qgis_easy_query
xcopy metadata.txt qgis_easy_query
xcopy i18n\qgis_easy_query_ru.ts qgis_easy_query\i18n\qgis_easy_query_ru.ts
lrelease qgis_easy_query\i18n\qgis_easy_query_ru.ts
del qgis_easy_query\i18n\qgis_easy_query_ru.ts
zip -r qgis_easy_query.zip qgis_easy_query
del /s /q qgis_easy_query
rmdir /s /q qgis_easy_query