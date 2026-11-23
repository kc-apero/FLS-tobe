@echo off
setlocal enabledelayedexpansion
REM ===================================================================
REM  NUT MO MAN HINH FLS  --  UAT tren MAY NAY
REM
REM  Tep nay CO Y la ASCII thuan. Ky tu UTF-8 trong mot .cmd bi cmd.exe
REM  lam hong DONG LENH (da xay ra 10/09: 'ua-gio' is not recognized).
REM
REM  Bon lop, va lop nao hong thi NOI RO hong o dau:
REM    1. Docker + PostgreSQL co song khong
REM    2. Khoa ky the (FLS_JWT_SECRET) -- sinh va LUU neu chua co
REM    3. Dung may tren 127.0.0.1:8088
REM    4. Mo trinh duyet
REM
REM  Dong cua so nay la TAT may. Ctrl+C cung duoc.
REM ===================================================================
cd /d "%~dp0"
echo.
echo ================= NUT MO MAN HINH FLS =================
echo.

REM ---------- Lop 1: kho ----------
echo [1/4] Kiem kho PostgreSQL...
docker exec fls-pg-1 pg_isready -U fls -d fls >nul 2>&1
if errorlevel 1 (
  echo     kho chua song -- dang bat Docker Compose...
  docker compose up -d >nul 2>&1
  set /a N=0
  :CHO
  set /a N+=1
  docker exec fls-pg-1 pg_isready -U fls -d fls >nul 2>&1
  if not errorlevel 1 goto KHO_OK
  if !N! geq 30 (
    echo.
    echo   KHONG BAT DUOC KHO sau 30 lan thu.
    echo   Kiem tra Docker Desktop da chay chua, roi bam lai nut nay.
    echo.
    pause
    exit /b 1
  )
  %SystemRoot%\System32\timeout.exe /t 2 /nobreak >nul
  goto CHO
)
:KHO_OK
echo     kho OK.

REM ---------- Lop 2: khoa ky the ----------
REM  Doc khoa DA LUU o muc `User` -- KHONG doc `%FLS_JWT_SECRET%` cua tien
REM  trinh. Mot bien vua duoc luu o muc User KHONG hien ra trong cac shell da
REM  mo truoc do, nen phep thu `if "%FLS_JWT_SECRET%"==""` se bao "chua co"
REM  va SINH LAI KHOA MOI moi lan bam -- ghi de len khoa cu trong im lang.
REM  Bat duoc 11/09 ngay tren log chay thu: no in "chua co" o lan bam THU HAI.
echo [2/4] Kiem khoa ky the (FLS_JWT_SECRET)...
REM  Doc thang tu so dang ky (`HKCU\Environment` = bien muc `User`). Thuan
REM  cmd -- KHONG nhoi PowerShell vao `for /f`, vi dau nhay long nhau giua
REM  cmd va PowerShell la cho hong im lang nhat tren Windows.
for /f "tokens=2,*" %%A in ('reg query HKCU\Environment /v FLS_JWT_SECRET 2^>nul ^| findstr /C:"FLS_JWT_SECRET"') do set "FLS_JWT_SECRET=%%B"
if "%FLS_JWT_SECRET%"=="" (
  echo     chua co -- dang sinh mot khoa moi va LUU cho tai khoan Windows nay...
  for /f "delims=" %%K in ('powershell -NoProfile -Command "$b=New-Object byte[] 48;[Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b);[Convert]::ToBase64String($b)"') do set "FLS_JWT_SECRET=%%K"
  powershell -NoProfile -Command "[Environment]::SetEnvironmentVariable('FLS_JWT_SECRET',$env:FLS_JWT_SECRET,'User')" >nul 2>&1
  echo     da sinh va luu. Lan sau dung lai khoa nay.
) else (
  echo     da co tu truoc -- dung lai, KHONG sinh khoa moi.
)

REM ---------- Lop 3: dung may ----------
echo [3/4] Dung may tren http://127.0.0.1:8088 ...
netstat -ano | findstr /C:"127.0.0.1:8088" | findstr /C:"LISTENING" >nul 2>&1
if not errorlevel 1 (
  echo.
  echo   DA CO MOT MAY DANG NGHE CONG 8088.
  echo   Hai may cung mot cong thi KHONG BIET CAI NAO DANG TRA LOI
  echo   -- da gap 11/09: may cu tra ket qua cu sau khi da va code.
  echo   Dong cua so den kia truoc roi bam lai nut nay.
  echo.
  pause
  exit /b 1
)

REM ---------- Lop 4: mo trinh duyet ----------
echo [4/4] Mo trinh duyet sau 5 giay...
start "" /b cmd /c "%SystemRoot%\System32\timeout.exe /t 5 /nobreak >nul & start http://127.0.0.1:8088/"

echo.
echo =======================================================
echo   Man hinh: http://127.0.0.1:8088/
echo   Nguoi dang lam: dungtt1@apero.vn
echo.
echo   *** DUONG GHI DANG MO (--cho-ghi) ***
echo   Moi cu bam GHI THAT vao so ke toan. `fls_itl` la
echo   append-only: dong da vao thi KHONG xoa duoc, chi
echo   ghi them dong sua. Day la CO Y -- mot buoi UAT ma
echo   moi nut tra 405 thi khong chung minh duoc gi.
echo.
echo   DONG CUA SO NAY LA TAT MAY.
echo =======================================================
echo.

set PYTHONUTF8=1
.venv\Scripts\python.exe tools\chay_cua.py --cho-web --cho-ghi --actor dungtt1@apero.vn

echo.
echo May da dung.
pause
