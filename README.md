# Tiny Monte Carlo

Laboratorios para el problema de Tiny Montecarlo (Computación Paralela 2021 - FAMAF)

- [Página en Wikipedia sobre el problema](https://en.wikipedia.org/wiki/Monte_Carlo_method_for_photon_transport)
- [Código original](https://omlc.org/software/mc/) de [Scott Prahl](https://omlc.org/~prahl/)

Integrantes:
* Javier Cremona
* Marcelo Castillo


## Laboratorio 1
* [Presentación](https://youtu.be/oZRH8gufSP4)
* Ver `doc/informe1` 

### Dependencias
* python3
* gcc/clang

### Código Entregado
```
git checkout tags/Lab1Entrega
```
Para correr el código (por ej. realizar 10 corridas):
```
./execute_n_times.sh 10
```
Para esta versión solo corre con gcc. Corre con `-O3 -ffast-math -march=native` y FDO. 
Ver `python/config_flags.py` y `python/execute_n_times.py` para configurar otras banderas. 

Para explorar las banderas (lo que se mostró en el informe)
```
./explore_flags.sh
```

### Código corregido
```
git checkout tags/Lab1Corregido
```
Cambiamos el generador de números aleatorios, ahora implementamos y usamos PCG.
Para correr:
```
./execute_n_times.sh <COMPILER> <N>
```
donde `COMPILER` es `gcc` o `clang` y `N` es la cantidad de veces que se va a ejecutar `tiny_mc`.
Corre con `-O3 -ffast-math -march=native` y FDO.
Ver `python/config_flags.py` y `python/execute_n_times.py` para configurar otras banderas.

## Laboratorio 2
* [Presentación](https://youtu.be/xeBgcsJLczs)
* Ver `doc/informe2` 

### Dependencias
* python3
* gcc
* clang
* icc
* ispc
* llvm-profdata

### Código Entregado
Agregamos `icc` a lista de compiladores que se pueden usar.
En este laboratorio buscamos vectorizar. Probamos 3 implementaciones: una con ISPC
 y dos en las que buscamos que el compilador autovectorice. En `doc/informe2` 
 están los resultados de las corridas en el servidor de FAMAF conocido como `jupiterace`. 

* ISPC
    ```
    git checkout tags/Lab2ISPC
    ```
* Versión Rand-Offline
    ```
    git checkout tags/Lab2RandOffline
    ```
* Versión Rand-Ondemand
    ```
    git checkout tags/Lab2RandOndemand
    ```  
  
Para correr:
```
./execute_n_times.sh <COMPILER> <N>
```
donde `COMPILER` es `gcc`,`clang` o `icc` y `N` es la cantidad de veces que se va a ejecutar `tiny_mc`.

## Laboratorio 3
* [Presentación](https://youtu.be/Q809NeAs9Eg)
* Ver `doc/informe3` 

### Dependencias
* python3
* gcc
* icc

### Código Entregado
Cambiamos mínimamente el código para usar OpenMP (ver Presentación). Se agregan scripts de Slurm para correr en los servidores.
Para ver esta versión:
```
git checkout tags/Lab3OMP
```

Para correr la versión con OpenMP:
```
OMP_NUM_THREADS=<N_THREADS> ./execute_n_times.sh -p -n <N> <COMPILER>
```
donde `N_THREADS` es la cantidad de hilos a usar, `COMPILER` es `gcc`,`clang` o `icc` 
y `N` es la cantidad de veces que se va a ejecutar `tiny_mc`.

Para correr la versión secuencial hay que remover la bandera `-p`. La versión secuencial no usa OpenMP, 
notar que no es lo mismo que usar `OMP_NUM_THREADS=1`, pues esto implicaría usar OpenMP y agregar trabajo extra.
Por lo tanto, para correr la versión secuencial:
```
./execute_n_times.sh -n <N> <COMPILER>
```

## Laboratorio 4
* [Presentación](https://youtu.be/I8k47GMEWf4)
* Ver `doc/informe4`

### Dependencias
* python3
* cuda
* nvcc

### Código Entregado
Portamos el problema a CUDA. Nos basamos en la versión de Lab 1 corregida.
Para ver esta versión:
```
git checkout tags/Lab4CUDA
```

Para correr esta versión:
```
./execute_cuda_n_times.sh -n <N>
```

donde `N` es la cantidad de veces que se va a ejecutar `tiny_mc`. Para ejecutar una versión que recorre
distintos tamaños de bloque y distinta cantidad de fotones por hilo, y genera un heatmap:
```
./execute_cuda_n_times.sh -x -n <N>
```

Para correr el profiling que genera un reporte completo (incluye roofline):
```
ncu -f -o tiny_kernel --set full ./tiny_mc
```

Ver `submit_nsight.sh` para ver cómo correrlo en los servidores de FAMAF (porque hay que cambiar la variable de entorno TMPDIR).
Luego usar `ncu-ui` para ver el reporte en una interfaz gráfica (usar x2go para levantar ventanas gráficas en los servidores de FAMAF).
También se puede hacer que el profiling mida eventos específicos en lugar de reportar toda la información. 

**NOTA:** `ncu` y `ncu-ui` se suelen encontrar en `/opt/cuda/11.2.2/nsight-compute-2020.3.1/`. 

Otras herramientas útiles son `nvprof` (para ver si están ejecutando los kernels), `cuobjdump` (nos muestra para que arquitectura se compiló) 
y `cuda-memcheck` (ver problemas de memoria).
`nvprof` en las versiones nuevas corre como parte de `nsight`.  