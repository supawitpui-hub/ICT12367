<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>บันทึกข้อมูลพนักงาน</title>
</head>
<body>
    <div class="container my-3">
    <h2 class="text-center">แบบฟอร์มบันทึกข้อมูลพนักงาน</h2>
    <form action="L5insertData.php" method="POST">
        <div class="form-group mb-3">
            <label for="">ชื่อ</label>
            <input type="text" name="fname" id="" class="form-control">
        </div>
        <div class="form-group mb-3">
            <label for="">นามสกุล</label>
            <input type="text" name="lname" id="" class="form-control">
        </div>
        <div class="form-group mb-3">
            <label for="gender">เพศ</label>
            <input type="radio" name="gender" value="male">ชาย
            <input type="radio" name="gender" value="female">หญิง
            <input type="radio" name="gender" value="other">อื่นๆ
        </div>
        <div class="form-group mb-3">
            <label for="">ทักษะ</label>
            <input type="checkbox" name="skills[]" value="Java"> Java
            <input type="checkbox" name="skills[]" value="PHP"> PHP
            <input type="checkbox" name="skills[]" value="Python"> Python
            <input type="checkbox" name="skills[]" value="HTML"> HTML
        </div>
        <input type="submit" value="บันทึกข้อมูล" class="btn btn-success">
        <input type="reset" value="ล้างข้อมูล" class="btn btn-danger">
        <a href="L5index.php" class="btn btn-primary">กลับไปหน้าแรก</a>
    </form>
    </div>
</body>
</html>