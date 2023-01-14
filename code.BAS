100 REM //////////////////////////////////////////////////////////
110 REM // Name: Peter M. Maurer
120 REM // Program: Sieve of Eratosthenes
130 REM // Due: Never
140 REM // Language: Dartmouth Basic
150 REM //////////////////////////////////////////////////////////
153 REM Modlines: 260,290,300,370,470
157 REM Change THEN to GOTO for YABASIC
160 DIM C(999)
170 REM define the sieve data structure
180 FOR I = 0 TO 999
190 REM everything is potentially prime until proven otherwise
200 LET C(I) = 1
210 NEXT I
220 REM Neither 1 nor 0 is prime, so flag them off
225 LET C(0) = 0
230 LET C(1) = 0
240 REM start the sieve with the integer 0
250 LET I = 0
260 IF I>=1000 THEN 440
270 REM advance to the next un-crossed out number.
280 REM this number must be a prime
290 IF I >= 1000 THEN 440
300 IF C(I) <> 0 THEN 330
310 LET I = I+1
320 GOTO 290
330 REM come here when prime found
340 REM cross out all multiples of the prime, starting with 2*p.
350 LET J = 2
360 LET P = I * J
370 IF P >= 1000 THEN 420
380 LET C(P) = 0
390 LET J = J+1
400 LET P = I * J
410 GOTO 370
420 LET I = I+1
430 GOTO 260
440 REM all uncrossed-out numbers are prime
450 REM print all primes
460 FOR I = 0 TO 999
470 IF C(I) = 0 THEN 490
480 PRINT I," is prime"
490 NEXT I
500 END