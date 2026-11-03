@echo off
rem ═══════════════════════════════════════════════════════════════════════
rem  nhip_chup.cmd — cai ma BO HEN GIO cua Windows goi (`QĐ-ITL-114`).
rem
rem  ⛔⛔ Vi sao co tep nay chu ⛔ khong nhoi moi thu vao mot dong `schtasks`:
rem
rem    ⓐ `schtasks /TR` la MOT chuoi, va dau ngoac kep long nhau trong do la
rem      cho **de hong nhat** — hong theo kieu *"task tao xong, chay ra ma
rem      loi 1 moi gio"*, va ⛔ khong ai doc thong bao cua no.
rem    ⓑ Bo hen gio ⛔ khong dat THU MUC LAM VIEC. `nhip_chup.py` tu chen goc
rem      kho vao `sys.path`, nhung `gcloud` va cac duong tuong doi khac thi
rem      ⛔ khong — nen `cd /d` o day la mot dong RE de mua mot lop an toan.
rem    ⓒ ⭐ Va quan trong nhat: **dau ra phai duoc GIU LAI**. Mot lan chay
rem      hong trong im lang la dung cai `A1` sinh ra de tranh — nhip dung, va
rem      con so *"anh moi gio"* van dung vi ⛔ khong ai dem lai.
rem
rem  ⭐ Co `--tu-bo-hen-gio` la thu **phan biet mot luot TU CHAY voi mot luot
rem    GO TAY**: chi cu goi mang co nay duoc ghi `actor = nhip@fls`, va cong
rem    `A1` dem **dung** actor ay. ⛔ Bo co nay ra thi cong `A1` **thoi do
rem    duoc** thu no dang do.
rem ═══════════════════════════════════════════════════════════════════════
setlocal
set FLS=%~dp0..
cd /d "%FLS%" || exit /b 9

rem ⛔⛔ `PYTHONUTF8=1` — ⛔ khong phai cho dep. Luot chay dau tien qua bo hen
rem   gio ghi log ra **mojibake** (`Â·`, `â›”`): Python lay trang ma he
rem   thong khi ⛔ khong co bien nay, va mot log ⛔ khong doc duoc la mot log
rem   **⛔ khong ai doc** — dung cai `A1` sinh ra de tranh.
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

rem ⚠ Mot tep ghi/thang, ⛔ khong xoay vong: mot luot in ~40 dong, 12 luot/ngay
rem   ⇒ ~175k dong/nam. Neu no thanh van de thi do la mot van de CO SO DO, va
rem   luc ay hay xoay vong — ⛔ dung doan truoc.
if not exist "%FLS%\.nhip" mkdir "%FLS%\.nhip"
set LOG=%FLS%\.nhip\nhip_chup.log

echo. >> "%LOG%"
echo ===== %DATE% %TIME% ===== >> "%LOG%"
"%FLS%\.venv\Scripts\python.exe" tools\nhip_chup.py --that --tu-bo-hen-gio >> "%LOG%" 2>&1
set MA=%ERRORLEVEL%
echo ----- ma tra ve: %MA% >> "%LOG%"

rem ⛔ Tra lai DUNG ma cua Python: `3` = co lan HONG. Bo hen gio ghi ma nay
rem   vao *"Last Run Result"*, nen mot lan hong **doc lai duoc** ma ⛔ khong
rem   phai mo tep log.
exit /b %MA%
