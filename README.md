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
./execute_n_times <COMPILER> <N>
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
./execute_n_times <COMPILER> <N>
```
donde `COMPILER` es `gcc`,`clang` o `icc` y `N` es la cantidad de veces que se va a ejecutar `tiny_mc`.
