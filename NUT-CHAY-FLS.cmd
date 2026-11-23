@echo off
rem =====================================================================
rem  NUT-CHAY-FLS.cmd -- MOT NUT de owner bam (tam thoi, owner y/c 10/09).
rem
rem  Bam doi chuot vao tep nay. Khong can dong lenh, khong can Dev.
rem
rem  !! NUT NAY CHI CHUP, KHONG NAP VAO SO. Ly do la mot cong CHAN, khong
rem     phai mot thieu sot: nap tang `R |` len so hien tai sinh +6.617 dong
rem     va 3.694 dong TRUNG (da do tren kho nhap 10/09). Nap chi mo sau khi
rem     khoang lech 3.413 dong duoc giai thich TUNG DONG.
rem
rem  Bon lop, moi lop noi ro no dang lam gi -- mot nut im lang roi bao
rem  "xong" la dung cai cong A1 sinh ra de tranh:
rem    (a) kho PostgreSQL co song -- bat neu chua, CHO toi khi no tra loi
rem    (b) token Google Sheets con han
rem    (c) chup CA HAI lan (Bank + PM), actor = nhip@fls(tay)
rem    (d) bao cao mot mat: so bao nhieu dong, anh da nap chua, nguon rong
rem
rem  !! TEP NAY PHAI LA ASCII THUAN. cmd.exe doc tep batch theo codepage
rem     OEM, nen mot ky tu UTF-8 (dau tieng Viet, khung ke, bieu tuong)
rem     BAM NAT ca dong lenh chua no -- ban dau tien cua tep nay da hong
rem     dung cach ay ("ua-gio is not recognized"). `tools/nhip_chup.cmd`
rem     vua ASCII thuan chinh vi ly do nay.
rem
rem  --bo-qua-gio : nhip tu bo luot khi gio dong ho nay da co anh. Mot NUT
rem                 bam vao khong lam gi thi khong phai mot nut => co nay
rem                 bat buoc phai co o day.
rem  --tu-bo-hen-gio : CO Y KHONG DUNG. No ghi actor = nhip@fls va cong A1
rem                 dem theo actor ay; mot luot go tay deo nhan tu-dong la
rem                 tu bam cho cong xanh. May cung tu choi co nay khi go tay.
rem =====================================================================
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
set FLS=%~dp0
cd /d "%FLS%" || exit /b 9
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PY=%FLS%.venv\Scripts\python.exe

echo.
echo ==========================================================
echo   FLS - MOT NUT   (chi CHUP, khong nap vao so)
echo   %DATE% %TIME%
echo ==========================================================

echo.
echo [1/4] Kho PostgreSQL...
docker ps --filter "name=fls-pg-1" --filter "status=running" --format "{{.Names}}" 2>nul | findstr /i "fls-pg-1" >nul
if !ERRORLEVEL!==0 (
  echo       kho DANG CHAY.
  goto TOKEN
)
rem Vong cho dat NGOAI khoi ( ) -- mot nhan `:` trong khoi la mot cho hong
rem nua cua .cmd: `goto` nhay ra khoi khoi va phan con lai bi bo.
echo       kho chua chay - dang bat Docker + kho...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe" >nul 2>&1
docker compose up -d pg >nul 2>&1
set /a N=0
:CHO
set /a N+=1
docker exec fls-pg-1 pg_isready -U fls -d fls >nul 2>&1
if !ERRORLEVEL!==0 goto KHO_OK
if !N! GEQ 60 (
  echo       [LOI] KHO KHONG LEN sau ~2 phut.
  echo             Mo Docker Desktop bang tay roi bam lai nut nay.
  goto CUOI
)
ping -n 3 127.0.0.1 >nul
goto CHO
:KHO_OK
echo       kho DA LEN.

:TOKEN
echo.
echo [2/4] Token Google Sheets...
"%PY%" -c "import sys;sys.path.insert(0,'.');from tools.do_hinh_dang import token;token()" >nul 2>&1
if not !ERRORLEVEL!==0 (
  echo       [LOI] KHONG LAY DUOC TOKEN.
  echo             Chay mot lan:  gcloud auth login
  echo             Roi bam lai nut nay.
  goto CUOI
)
echo       token OK.

echo.
echo [3/4] Chup ca hai lan (Bank + PM)...
if not exist "%FLS%.nhip" mkdir "%FLS%.nhip"
"%PY%" tools\nhip_chup.py --that --bo-qua-gio
set MA=!ERRORLEVEL!
if not !MA!==0 (
  echo.
  echo       [LOI] CO LAN CHUP HONG - ma tra ve !MA!. Doc phan `loi` o tren.
  echo             Hay gap nhat: mot sheet vua bi DOI TEN, ban khai mo coi.
)

echo.
echo [4/4] Bao cao trang thai...
"%PY%" tools\nut_trang_thai.py

:CUOI
echo.
echo ==========================================================
echo   Xong. Bam mot phim bat ky de dong cua so nay.
echo ==========================================================
pause >nul
endlocal
