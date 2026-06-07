# Guía práctica de comandos Git

## 1. Conceptos básicos

Git permite controlar los cambios de un proyecto y sincronizarlos con un repositorio remoto, por ejemplo GitHub.

En un flujo normal intervienen tres zonas principales:

| Zona | Qué es |
|---|---|
| Carpeta de trabajo | Los ficheros reales que está modificando en su ordenador |
| Área de preparación, o `staging area` | Cambios que ya ha seleccionado para incluir en el próximo commit |
| Repositorio local | Historial de commits guardado en su ordenador |
| Repositorio remoto | Copia alojada en GitHub, GitLab, Bitbucket u otra plataforma |

El flujo habitual es:

```bash
git status
git add .
git commit -m "Mensaje del commit"
git push
```

---

# 2. Comandos básicos de consulta

## `git status`

Muestra el estado actual del repositorio.

```bash
git status
```

Sirve para saber:

- En qué rama está.
- Si hay ficheros modificados.
- Si hay ficheros nuevos no controlados por Git.
- Si hay cambios pendientes de commit.
- Si la rama local está sincronizada con GitHub.

Ejemplo de repositorio limpio:

```bash
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Esto significa que no hay cambios pendientes y que la rama local está sincronizada con la rama remota.

---

## `git log`

Muestra el historial de commits.

```bash
git log
```

Versión resumida:

```bash
git log --oneline
```

Versión resumida con ramas y remoto:

```bash
git log --oneline --decorate -5
```

Ejemplo:

```bash
a1b2c3d (HEAD -> main, origin/main) Actualiza cambios locales
```

Si `HEAD -> main` y `origin/main` aparecen en el mismo commit, significa que la rama local y GitHub están sincronizados.

---

## `git diff`

Muestra los cambios realizados en los ficheros antes de añadirlos al área de preparación.

```bash
git diff
```

Sirve para revisar qué ha cambiado antes de hacer `git add`.

Para ver los cambios ya añadidos al área de preparación:

```bash
git diff --staged
```

---

# 3. Añadir cambios

## `git add`

Añade cambios al área de preparación.

Añadir todos los cambios:

```bash
git add .
```

Añadir un fichero concreto:

```bash
git add nombre-del-fichero.md
```

Añadir una carpeta concreta:

```bash
git add carpeta/
```

`git add .` incluye:

- Ficheros modificados.
- Ficheros nuevos.
- Ficheros eliminados.

Después de ejecutar `git add`, puede comprobar qué va a entrar en el commit con:

```bash
git status
```

---

# 4. Crear commits

## `git commit`

Guarda los cambios preparados en el historial local del repositorio.

```bash
git commit -m "Mensaje descriptivo del cambio"
```

Ejemplo:

```bash
git commit -m "Actualiza documentación del proyecto"
```

Un buen mensaje de commit debería explicar brevemente qué se ha cambiado.

Ejemplos recomendables:

```bash
git commit -m "Añade guía inicial de instalación"
git commit -m "Corrige enlaces del índice"
git commit -m "Actualiza configuración de GitHub Pages"
git commit -m "Añade nuevos capítulos al libro"
```

Ejemplos menos recomendables:

```bash
git commit -m "cambios"
git commit -m "cosas"
git commit -m "update"
```

---

# 5. Subir cambios a GitHub

## `git push`

Sube los commits locales al repositorio remoto.

```bash
git push
```

Si la rama local ya está vinculada con GitHub, normalmente basta con ese comando.

En un primer push puede ser necesario indicar rama y remoto:

```bash
git push -u origin main
```

El parámetro `-u` deja vinculada la rama local con la rama remota. Después de eso, normalmente bastará con:

```bash
git push
```

---

# 6. Traer cambios desde GitHub

## `git pull`

Trae los cambios del repositorio remoto y los integra en su rama local.

```bash
git pull
```

Se usa cuando GitHub tiene cambios que todavía no existen en su copia local.

Por ejemplo, si al hacer `git push` aparece un mensaje indicando que el remoto contiene trabajo que usted no tiene, puede hacer:

```bash
git pull
git push
```

---

## `git fetch`

Consulta los cambios del remoto, pero no los integra automáticamente en su rama local.

```bash
git fetch
```

Después puede revisar diferencias entre la rama local y la remota.

Ejemplo:

```bash
git log --oneline --decorate --all --graph
```

Diferencia práctica:

| Comando | Qué hace |
|---|---|
| `git fetch` | Descarga información del remoto, pero no modifica sus ficheros |
| `git pull` | Descarga información del remoto y la integra en su rama actual |

En el trabajo diario, si está trabajando solo en el repositorio, normalmente puede usar directamente:

```bash
git pull
```

---

# 7. Trabajar con ramas

## Ver ramas

```bash
git branch
```

La rama activa aparece con un asterisco:

```bash
* main
  develop
```

Ver ramas locales y remotas:

```bash
git branch -a
```

Si el resultado se queda en pantalla y no vuelve a la consola, probablemente Git ha abierto un paginador. Para salir, pulse:

```text
q
```

---

## Cambiar de rama

```bash
git checkout nombre-rama
```

Forma moderna equivalente:

```bash
git switch nombre-rama
```

Ejemplo:

```bash
git switch develop
```

---

## Crear una rama nueva

```bash
git switch -c nombre-rama
```

Ejemplo:

```bash
git switch -c feature/nueva-documentacion
```

---

# 8. Clonar un repositorio

## `git clone`

Descarga un repositorio remoto a su ordenador.

```bash
git clone URL_DEL_REPOSITORIO
```

Ejemplo:

```bash
git clone https://github.com/usuario/repositorio.git
```

Después debe entrar en la carpeta creada:

```bash
cd repositorio
```

Y puede comprobar el estado:

```bash
git status
```

---

# 9. Ver la configuración remota

## `git remote -v`

Muestra con qué repositorio remoto está conectado su proyecto local.

```bash
git remote -v
```

Ejemplo:

```bash
origin  https://github.com/usuario/repositorio.git (fetch)
origin  https://github.com/usuario/repositorio.git (push)
```

---

# 10. Procedimiento concreto: subir cambios locales a GitHub

Este es el caso habitual cuando ha trabajado en VS Code, ha modificado ficheros y ha creado ficheros nuevos.

## Paso 1. Abrir terminal en la carpeta del proyecto

Desde VS Code:

```text
Terminal > New Terminal
```

O desde el Explorador de archivos de Windows:

1. Abra la carpeta del proyecto.
2. Haga clic en la barra de dirección.
3. Escriba:

```bash
cmd
```

4. Pulse `Enter`.

También puede hacer clic derecho en la carpeta y elegir:

```text
Abrir en Terminal
```

---

## Paso 2. Comprobar el estado

```bash
git status
```

Puede ver ficheros modificados:

```bash
modified:   README.md
```

Y ficheros nuevos:

```bash
Untracked files:
  nuevo_capitulo.md
```

En VS Code, los ficheros nuevos suelen aparecer en verde. Cuando ya se añaden, se confirman y no tienen cambios pendientes, pasan a verse normalmente en blanco.

---

## Paso 3. Añadir todos los cambios

```bash
git add .
```

Esto añade al próximo commit:

- Ficheros modificados.
- Ficheros nuevos.
- Ficheros eliminados.

---

## Paso 4. Revisar lo que se va a confirmar

```bash
git status
```

Ahora los cambios deberían aparecer como preparados para commit.

---

## Paso 5. Crear el commit

```bash
git commit -m "Actualiza cambios del proyecto"
```

Puede usar un mensaje más específico, por ejemplo:

```bash
git commit -m "Añade nuevos ficheros de documentación"
```

---

## Paso 6. Subir los cambios a GitHub

```bash
git push
```

Si es la primera vez que sube esa rama:

```bash
git push -u origin main
```

---

## Paso 7. Comprobar que todo está actualizado

```bash
git status
```

El resultado esperado es:

```bash
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

También puede comprobarlo con:

```bash
git log --oneline --decorate -5
```

Si ve algo parecido a esto:

```bash
a1b2c3d (HEAD -> main, origin/main) Actualiza cambios del proyecto
```

significa que la rama local y la rama remota de GitHub apuntan al mismo commit.

---

# 11. Procedimiento concreto: actualizar mi copia local con lo que hay en GitHub

Si quiere traer a su ordenador los cambios que están en GitHub:

```bash
git status
git pull
git status
```

Si no tiene cambios locales pendientes, el proceso suele ser directo.

Si tiene cambios locales pendientes, es recomendable revisarlos antes:

```bash
git status
```

Si quiere conservarlos:

```bash
git add .
git commit -m "Guarda cambios locales antes de actualizar"
git pull
```

---

# 12. Procedimiento concreto: he creado ficheros nuevos y no aparecen en GitHub

Compruebe el estado:

```bash
git status
```

Si aparecen como `Untracked files`, Git todavía no los está siguiendo.

Solución:

```bash
git add .
git commit -m "Añade nuevos ficheros"
git push
```

Después compruebe:

```bash
git status
```

Resultado esperado:

```bash
nothing to commit, working tree clean
```

---

# 13. Procedimiento concreto: GitHub tiene cambios y no me deja hacer push

Puede aparecer un error al hacer:

```bash
git push
```

Indicando que el remoto contiene cambios que usted no tiene.

En ese caso:

```bash
git pull
git push
```

Si aparecen conflictos, Git indicará qué ficheros debe revisar. Después de resolverlos:

```bash
git add .
git commit -m "Resuelve conflictos"
git push
```

---

# 14. Procedimiento concreto: quiero saber en qué rama estoy

```bash
git branch
```

O también:

```bash
git status
```

Ejemplo:

```bash
On branch main
```

Eso indica que está en la rama `main`.

---

# 15. Procedimiento concreto: quiero ver si mi rama local y GitHub están sincronizados

Ejecute:

```bash
git status
```

Y después:

```bash
git log --oneline --decorate -5
```

Debe buscar algo parecido a:

```bash
(HEAD -> main, origin/main)
```

Si `HEAD -> main` y `origin/main` están juntos, su rama local y GitHub están sincronizados.

---

# 16. Procedimiento concreto: quiero subir por primera vez un repositorio local a GitHub

Primero cree el repositorio vacío en GitHub.

Después, en la carpeta local:

```bash
git init
git add .
git commit -m "Primer commit"
git branch -M main
git remote add origin https://github.com/usuario/repositorio.git
git push -u origin main
```

Explicación:

| Comando | Qué hace |
|---|---|
| `git init` | Convierte la carpeta en un repositorio Git |
| `git add .` | Añade todos los ficheros |
| `git commit -m "Primer commit"` | Crea el primer commit |
| `git branch -M main` | Renombra la rama principal a `main` |
| `git remote add origin ...` | Conecta el repositorio local con GitHub |
| `git push -u origin main` | Sube la rama `main` a GitHub y deja la vinculación configurada |

---

# 17. Procedimiento concreto: he añadido un fichero demasiado grande por error

GitHub no permite subir ficheros de más de 100 MB en repositorios normales.

Si todavía no ha hecho commit, puede quitarlo del área de preparación:

```bash
git restore --staged nombre-del-fichero
```

Y añadirlo al `.gitignore`:

```bash
echo nombre-del-fichero >> .gitignore
```

Después:

```bash
git add .gitignore
git commit -m "Ignora fichero grande"
```

Si ya hizo commit con el fichero grande, el caso es más delicado porque el fichero queda en el historial. En ese caso conviene revisar el caso concreto antes de continuar.

---

# 18. `.gitignore`

El fichero `.gitignore` sirve para indicar qué ficheros o carpetas no debe seguir Git.

Ejemplos habituales:

```gitignore
# Dependencias
node_modules/

# Ficheros temporales
*.tmp
*.log

# Bases de datos locales
*.db

# Configuración sensible
.env

# Carpetas de compilación
dist/
build/
target/
```

Después de modificar `.gitignore`:

```bash
git add .gitignore
git commit -m "Actualiza gitignore"
git push
```

Importante: si un fichero ya estaba siendo seguido por Git antes de añadirlo a `.gitignore`, Git lo seguirá controlando. Para dejar de seguirlo sin borrarlo del disco:

```bash
git rm --cached nombre-del-fichero
git commit -m "Deja de seguir fichero ignorado"
git push
```

---

# 19. Comandos de deshacer cambios

## Deshacer cambios no añadidos

Si ha modificado un fichero y quiere volver a la última versión confirmada:

```bash
git restore nombre-del-fichero
```

Para todos los ficheros:

```bash
git restore .
```

Cuidado: esto descarta cambios locales no confirmados.

---

## Sacar un fichero del área de preparación

Si ha hecho `git add` pero todavía no ha hecho commit:

```bash
git restore --staged nombre-del-fichero
```

Para todos:

```bash
git restore --staged .
```

Esto no borra los cambios. Solo los saca del área de preparación.

---

## Corregir el último commit

Si acaba de hacer un commit y quiere modificar el mensaje:

```bash
git commit --amend -m "Nuevo mensaje del commit"
```

Si quiere añadir un fichero olvidado al último commit:

```bash
git add fichero-olvidado.md
git commit --amend
```

Si ya había hecho `push`, tenga cuidado con `--amend`, porque reescribe el historial local.

---

# 20. Tabla resumen de comandos frecuentes

| Comando | Para qué sirve |
|---|---|
| `git status` | Ver el estado del repositorio |
| `git add .` | Preparar todos los cambios para commit |
| `git add fichero` | Preparar un fichero concreto |
| `git commit -m "mensaje"` | Crear un commit |
| `git push` | Subir commits a GitHub |
| `git pull` | Traer e integrar cambios desde GitHub |
| `git fetch` | Consultar cambios remotos sin integrarlos |
| `git log --oneline` | Ver historial resumido |
| `git log --oneline --decorate -5` | Ver últimos commits con ramas |
| `git branch` | Ver ramas locales |
| `git branch -a` | Ver ramas locales y remotas |
| `git switch rama` | Cambiar de rama |
| `git switch -c rama` | Crear y cambiar a una rama nueva |
| `git remote -v` | Ver repositorios remotos configurados |
| `git diff` | Ver cambios no preparados |
| `git diff --staged` | Ver cambios preparados |
| `git restore fichero` | Deshacer cambios locales de un fichero |
| `git restore --staged fichero` | Sacar un fichero del área de preparación |
| `git clone URL` | Descargar un repositorio remoto |

---

# 21. Chuleta rápida para el trabajo diario

## Subir cambios normales a GitHub

```bash
git status
git add .
git commit -m "Describe aquí el cambio"
git push
git status
```

---

## Actualizar mi copia local desde GitHub

```bash
git status
git pull
git status
```

---

## Ver si local y GitHub están sincronizados

```bash
git status
git log --oneline --decorate -5
```

---

## Crear una rama nueva de trabajo

```bash
git switch -c feature/nombre-del-cambio
```

---

## Volver a la rama principal

```bash
git switch main
```

---

## Traer cambios de GitHub antes de empezar a trabajar

```bash
git pull
```

---

# 22. Recomendación práctica

Antes de empezar a trabajar:

```bash
git pull
```

Mientras trabaja:

```bash
git status
```

Cuando quiera guardar y subir cambios:

```bash
git add .
git commit -m "Mensaje claro del cambio"
git push
```

Después de subir:

```bash
git status
git log --oneline --decorate -5
```

Si obtiene:

```bash
nothing to commit, working tree clean
```

y ve:

```bash
HEAD -> main, origin/main
```

entonces su proyecto local y GitHub están correctamente actualizados.
