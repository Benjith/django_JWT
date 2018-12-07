# Generated by Django 2.1.1 on 2018-12-07 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('BranchID', models.IntegerField(primary_key=True, serialize=False)),
                ('BranchCode', models.CharField(max_length=50)),
                ('BranchName', models.CharField(max_length=100)),
                ('Remarks', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('CountryID', models.IntegerField(primary_key=True, serialize=False)),
                ('CountryCode', models.CharField(max_length=50)),
                ('CountryName', models.CharField(max_length=100)),
                ('TimeZone', models.CharField(max_length=500)),
                ('Remarks', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('CustomerID', models.IntegerField(primary_key=True, serialize=False)),
                ('CustomerFName', models.CharField(max_length=100)),
                ('CustomerLName', models.CharField(max_length=100)),
                ('Address1', models.CharField(max_length=100)),
                ('Address2', models.CharField(max_length=100)),
                ('Email', models.CharField(max_length=100)),
                ('FirstLoggedDate', models.DateTimeField()),
                ('ExpiryDate', models.DateTimeField()),
                ('RenewalDate', models.DateTimeField()),
                ('CreatedDate', models.DateTimeField()),
                ('BranchID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Branch')),
                ('CountryID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Country')),
            ],
        ),
        migrations.CreateModel(
            name='DatabaseInfo',
            fields=[
                ('DatabaseInfoID', models.AutoField(primary_key=True, serialize=False)),
                ('DatabaseName', models.CharField(max_length=100)),
                ('Host', models.CharField(max_length=200)),
                ('Port', models.IntegerField()),
                ('Username', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Customers')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('ProductID', models.IntegerField(primary_key=True, serialize=False)),
                ('ProductName', models.CharField(max_length=100)),
                ('Remarks', models.CharField(max_length=200)),
                ('CreatedDate', models.DateTimeField()),
                ('BranchID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='RenewalDetails',
            fields=[
                ('RenewalDetailID', models.IntegerField(primary_key=True, serialize=False)),
                ('NoOfUsers', models.IntegerField()),
                ('RenewalDate', models.DateTimeField()),
                ('RenewalPeriodFrom', models.DateTimeField()),
                ('RenewalPeriodTo', models.DateTimeField()),
                ('BranchID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Branch')),
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Customers')),
                ('ProductID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Products')),
            ],
        ),
        migrations.CreateModel(
            name='RenewalUsers',
            fields=[
                ('RenewalUsersID', models.IntegerField(primary_key=True, serialize=False)),
                ('BranchID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Branch')),
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Customers')),
                ('ProductID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Products')),
                ('RenewalDetailID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.RenewalDetails')),
            ],
        ),
        migrations.CreateModel(
            name='UserLoggedDetails',
            fields=[
                ('UserLoggedDetailID', models.IntegerField(primary_key=True, serialize=False)),
                ('MACAddress', models.CharField(max_length=100)),
                ('IPAddress', models.CharField(max_length=100)),
                ('Logindatetime', models.DateTimeField()),
                ('Logoutdatatime', models.DateTimeField()),
                ('BranchID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('UserID', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.CharField(db_index=True, max_length=255, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('FirstLoggedDate', models.DateTimeField()),
                ('ExpiryDate', models.DateTimeField()),
                ('CreatedDate', models.DateTimeField()),
                ('IsActive', models.BooleanField(default=True)),
                ('IsAdmin', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField()),
                ('date_joined', models.DateTimeField()),
                ('is_superuser', models.BooleanField(default=False)),
                ('BranchID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Branch')),
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Customers')),
                ('ProductID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Products')),
            ],
        ),
        migrations.AddField(
            model_name='userloggeddetails',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Users'),
        ),
        migrations.AddField(
            model_name='renewalusers',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Users'),
        ),
        migrations.AddField(
            model_name='databaseinfo',
            name='ProductID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polosysCRM.Products'),
        ),
    ]
