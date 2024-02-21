from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('comintapp', '0010_lineofcredit_locnegotiationrequest_locconfirmation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrequest',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Loan amount in USD', max_digits=6),
        ),
    ]